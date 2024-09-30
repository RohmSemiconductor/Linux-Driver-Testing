-- This file is part of Buildbot.  Buildbot is free software: you can
-- redistribute it and/or modify it under the terms of the GNU General Public
-- License as published by the Free Software Foundation, version 2.
--
-- This program is distributed in the hope that it will be useful, but WITHOUT
-- ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
-- FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
-- details.
--
-- You should have received a copy of the GNU General Public License along with
-- this program; if not, write to the Free Software Foundation, Inc., 51
-- Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
--
-- Copyright Buildbot Team Members

BEGIN;

-- Delete soucestamps older than %s days.
-- The starting point is not "now" but the most recent sourcestamp.
DELETE FROM sourcestamps
WHERE created_at < (SELECT max(created_at) - (14 * 24 * 60 * 60) FROM sourcestamps);

DELETE FROM patches WHERE id NOT IN (SELECT patchid FROM sourcestamps);

-- Delete changes with no link to a sourcestamp.
UPDATE changes SET parent_changeids = NULL
WHERE parent_changeids IN (SELECT changeid FROM changes
        WHERE sourcestampid NOT IN (SELECT id FROM sourcestamps));

DELETE FROM changes
WHERE sourcestampid NOT IN (SELECT id FROM sourcestamps);

DELETE FROM change_files
WHERE changeid NOT IN (SELECT changeid FROM changes);

DELETE FROM change_properties
WHERE changeid NOT IN (SELECT changeid FROM changes);

DELETE FROM change_users
WHERE changeid NOT IN (SELECT changeid FROM changes);

DELETE FROM scheduler_changes
WHERE changeid NOT IN (SELECT changeid FROM changes);

-- Delete buildsets that have no link to a sourcestamp.
DELETE FROM buildset_sourcestamps
WHERE sourcestampid NOT IN (SELECT id FROM sourcestamps);

DELETE FROM buildsets
WHERE id NOT IN (SELECT buildsetid FROM buildset_sourcestamps);

DELETE FROM buildset_properties
WHERE buildsetid NOT IN (SELECT id FROM buildsets);

DELETE FROM buildrequests
WHERE buildsetid NOT IN (SELECT id FROM buildsets);

DELETE FROM buildrequest_claims
WHERE brid NOT IN (SELECT id FROM buildrequests);

UPDATE buildsets SET parent_buildid = NULL, parent_relationship = NULL
WHERE parent_buildid IN (SELECT id FROM builds
        WHERE buildrequestid NOT IN (SELECT id FROM buildrequests));

DELETE FROM builds
WHERE buildrequestid NOT IN (SELECT id FROM buildrequests);

DELETE FROM build_properties
WHERE buildid NOT IN (SELECT id FROM builds);

DELETE FROM steps
WHERE buildid NOT IN (SELECT id FROM builds);

DELETE FROM logs
WHERE stepid NOT IN (SELECT id FROM steps);

DELETE FROM logchunks
WHERE logid NOT IN (SELECT id FROM logs);

-- Delete non-active builders that are not referenced by any build.
DELETE FROM builders
WHERE id NOT IN (SELECT builderid FROM builder_masters)
AND id NOT IN (SELECT builderid FROM builds);

-- Delete tags not referenced by any builder.
DELETE FROM builders_tags
WHERE builderid NOT IN (SELECT id FROM builders);

DELETE FROM tags
WHERE id NOT IN (SELECT tagid FROM builders_tags);

-- Delete non-active workers that are not referenced by any build.
DELETE FROM workers
WHERE id NOT IN (SELECT workerid FROM configured_workers)
AND id NOT IN (SELECT workerid FROM builds);

COMMIT;
