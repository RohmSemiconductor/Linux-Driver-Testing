from buildbot.plugins import util, steps
factory_clean_db = util.BuildFactory()


def cleanup_db():
    factory_clean_db.addStep(steps.MasterShellCommand(
        command='sqlite3 state.sqlite < cleanupdb.sql && sqlite3 state.sqlite "VACUUM;"',
        name="Clean up database"
        ))

cleanup_db()
