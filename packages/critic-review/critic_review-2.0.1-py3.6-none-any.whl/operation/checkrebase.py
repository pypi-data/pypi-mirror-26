# -*- mode: python; encoding: utf-8 -*-
#
# Copyright 2012 Jens Lindström, Opera Software ASA
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

from operation import Operation, OperationResult, Optional

import dbutils
import gitutils
import reviewing.rebase
import changeset.utils as changeset_utils
import log.commitset

class CheckMergeStatus(Operation):
    def __init__(self):
        super(CheckMergeStatus, self).__init__({ "review_id": int,
                                                 "new_head_sha1": str,
                                                 "new_upstream_sha1": str })

    def process(self, db, user, review_id, new_head_sha1, new_upstream_sha1):
        review = dbutils.Review.fromId(db, review_id)
        upstreams = log.commitset.CommitSet(review.branch.getCommits(db)).getFilteredTails(review.repository)

        if len(upstreams) > 1:
            return OperationResult(rebase_supported=False)

        old_head = review.branch.getHead(db)
        old_upstream = gitutils.Commit.fromSHA1(db, review.repository, upstreams.pop())
        new_head = gitutils.Commit.fromSHA1(db, review.repository, new_head_sha1)
        new_upstream = gitutils.Commit.fromSHA1(db, review.repository, new_upstream_sha1)

        equivalent_merge = reviewing.rebase.createEquivalentMergeCommit(
            db, review, user, old_head, old_upstream, new_head, new_upstream)

        changesets = changeset_utils.createChangeset(
            db, user, review.repository, equivalent_merge, do_highlight=False)

        for changeset in changesets:
            if changeset.files:
                has_conflicts = True
                break
        else:
            has_conflicts = False

        return OperationResult(rebase_supported=True,
                               has_conflicts=has_conflicts,
                               merge_sha1=equivalent_merge.sha1)

class CheckConflictsStatus(Operation):
    def __init__(self):
        super(CheckConflictsStatus, self).__init__({ "review_id": int,
                                                     "merge_sha1": Optional(str),
                                                     "new_head_sha1": Optional(str),
                                                     "new_upstream_sha1": Optional(str) })

    def process(self, db, user, review_id, merge_sha1=None, new_head_sha1=None, new_upstream_sha1=None):
        review = dbutils.Review.fromId(db, review_id)

        if merge_sha1 is not None:
            merge = gitutils.Commit.fromSHA1(db, review.repository, merge_sha1)

            changesets = changeset_utils.createChangeset(
                db, user, review.repository, merge, conflicts=True, do_highlight=False)

            url = "/showcommit?repository=%d&sha1=%s&conflicts=yes" % (review.repository.id, merge.sha1)
        else:
            upstreams = review.getCommitSet(db).getFilteredTails(review.repository)

            if len(upstreams) > 1:
                return OperationResult(rebase_supported=False)

            old_head = review.branch.getHead(db)
            old_upstream = gitutils.Commit.fromSHA1(db, review.repository, upstreams.pop())
            new_head = gitutils.Commit.fromSHA1(db, review.repository, new_head_sha1)
            new_upstream = gitutils.Commit.fromSHA1(db, review.repository, new_upstream_sha1)

            replay = reviewing.rebase.replayRebase(db, review, user, old_head, old_upstream, new_head, new_upstream)

            changesets = changeset_utils.createChangeset(
                db, user, review.repository, from_commit=replay, to_commit=new_head, conflicts=True, do_highlight=False)

            url = "/showcommit?repository=%d&from=%s&to=%s&conflicts=yes" % (review.repository.id, replay.sha1, new_head.sha1)

        has_changes = False
        has_conflicts = False

        for changed_file in changesets[0].files:
            changed_file.loadOldLines()

            file_has_conflicts = False

            for chunk in changed_file.chunks:
                lines = changed_file.getOldLines(chunk)
                for line in lines:
                    if line.startswith("<<<<<<<"):
                        has_conflicts = file_has_conflicts = True
                        break
                if file_has_conflicts:
                    break

            if not file_has_conflicts:
                has_changes = True

        return OperationResult(has_conflicts=has_conflicts, has_changes=has_changes, url=url)

class CheckHistoryRewriteStatus(Operation):
    def __init__(self):
        super(CheckHistoryRewriteStatus, self).__init__({ "review_id": int,
                                                          "new_head_sha1": str })

    def process(self, db, user, review_id, new_head_sha1):
        review = dbutils.Review.fromId(db, review_id)

        old_head = review.branch.getHead(db)
        new_head = gitutils.Commit.fromSHA1(db, review.repository, new_head_sha1)

        mergebase = review.repository.mergebase([old_head, new_head])
        sha1s = review.repository.revlist([new_head], [mergebase])

        valid = True

        for sha1 in sha1s:
            commit = gitutils.Commit.fromSHA1(db, review.repository, sha1)
            if commit.tree == old_head.tree:
                break
        else:
            valid = False

        return OperationResult(valid=valid)
