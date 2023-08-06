# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Records integration for PIDRelations."""

from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PersistentIdentifier
from invenio_records.api import Record

from ..api import PIDConcept
from ..contrib.versioning import PIDVersioning
from ..utils import resolve_relation_type_config


class RecordDraft(PIDConcept):
    """Record Draft relationship.

    Users of this class should make calls to `link` and `unlink` based on their
    specific use-cases. Typical scenario is that of creating a new Deposit
    which is linked to a not-yet published record PID (PID status is RESERVED).
    Linking these two makes it possible for creating new record versions and
    having the abiltiy to track their deposits.

    NOTE: This relation exists because usually newly created records are not
    immediately stored inside the database (they have no `RecordMetada`). This
    leads to having deposits that are hanging onto no actual record and only
    possess "soft" links to their records' PIDs through metadata.
    """

    def __init__(self, child=None, parent=None, relation=None):
        """Create a record draft relation."""
        self.relation_type = resolve_relation_type_config('record_draft').id
        if relation is not None:
            if relation.relation_type != self.relation_type:
                raise ValueError('Provided PID relation ({0}) is not a '
                                 'version relation.'.format(relation))
            super(RecordDraft, self).__init__(relation=relation)
        else:
            # RecordDraft is composed of a one parent-child pair, hence we can
            # determine the child from the parent
            self.parent = parent
            self.child = child
            if parent:
                self.child = self.children.one_or_none()
            if child:
                self.parent = self.parents.one_or_none()
            # Run the parent class constructor in attempt to set the relation
            super(RecordDraft, self).__init__(
                child=self.child, parent=self.parent,
                relation_type=self.relation_type, relation=relation)

    @classmethod
    def link(cls, recid, depid):
        """Link a recid and depid."""
        recid_api = cls(parent=recid)
        depid_api = cls(child=depid)
        if recid_api.has_children:
            raise Exception('Recid {} already has a depid as a draft.'
                            .format(recid))
        if depid_api.parent:
            raise Exception('Depid {} already is a draft of a recid.'
                            .format(recid))
        recid_api.insert_child(depid)

    @classmethod
    def unlink(cls, recid, depid):
        """Unlink a recid and depid."""
        return cls(parent=recid).remove_child(depid)

    @classmethod
    def get_draft(cls, recid):
        """Get the draft of a record."""
        api = cls(parent=recid)
        if api.exists:
            return api.children.one_or_none()
        else:
            return None

    @classmethod
    def get_recid(cls, depid):
        """Get the recid of a record."""
        api = cls(child=depid)
        if api.exists:
            return api.parent
        else:
            return None


def get_latest_draft(recid_pid):
    """Return the latest draft for a record."""
    pv = PIDVersioning(child=recid_pid)
    if pv.draft_child:
        last_deposit = RecordDraft.get_draft(pv.draft_child)
    else:
        last_deposit = None
    return pv.last_child, last_deposit


def index_siblings(pid, include_pid=False, children=None,
                   neighbors_eager=False, eager=False, with_deposits=True):
    """Send sibling records of the passed pid for indexing.

    Note: By default does not index the 'pid' itself,
          only zero or more siblings.

    :param pid: PID (recid) of whose siblings are to be indexed.
    :param children: Overrides children with a fixed list of PID.
        Children should contain the 'pid' itself if 'neighbors_eager' is to
        be used, otherwise the last child is treated as the only neighbor.
    :param eager: Index all siblings immediately.
    :param include_pid: If True, will index also the provided 'pid'
           (default:False).
    :param neighbors_eager: Index the neighboring PIDs w.r.t. 'pid'
        immediately, and the rest with a bulk_index (default: False)
    :param with_deposits: Reindex also corresponding record's deposits.
    """
    assert not (neighbors_eager and eager), \
        "Only one of the 'eager' and 'neighbors_eager' flags can be set to " \
        "True, not both"
    if children is None:
        children = PIDVersioning(child=pid).children.all()

    objid = str(pid.object_uuid)
    children = [str(p.object_uuid) for p in children]

    idx = children.index(objid) if objid in children else len(children)

    # Split children (which can include the pid) into left and right siblings
    # If 'pid' is not in children, idx is the lenght of list, so 'left'
    # will be all children, and 'right' will be an empty list
    # [X X X] X [X X X]

    if include_pid:
        # [X X X X] [X X X]  Includes pid to the 'left' set
        left = children[:idx + 1]
    else:
        # [X X X] X [X X X]
        left = children[:idx]
    right = children[idx + 1:]

    if eager:
        eager_uuids = left + right
        bulk_uuids = []
    elif neighbors_eager:
        # neighbors are last of 'left' and first or 'right' siblings
        # X X [X] X [X] X X
        eager_uuids = left[-1:] + right[:1]
        # all of the siblings, except the neighbours
        # [X X] X X X [X X]
        bulk_uuids = left[:-1] + right[1:]
    else:
        eager_uuids = []
        bulk_uuids = left + right

    def get_dep_uuids(rec_uuids):
        """Get corresponding deposit UUIDs from record's UUIDs."""
        return [str(PersistentIdentifier.get('depid',
                    Record.get_record(id_)['_deposit']['id']).object_uuid)
                for id_ in rec_uuids]

    if with_deposits:
        eager_uuids += get_dep_uuids(eager_uuids)
        bulk_uuids += get_dep_uuids(bulk_uuids)

    for id_ in eager_uuids:
        RecordIndexer().index_by_id(id_)
    if bulk_uuids:
        RecordIndexer().bulk_index(bulk_uuids)
