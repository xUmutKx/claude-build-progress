# build-progress

A small Claude Code plugin that tells you where your Gradle build is, without leaving the terminal.

Type `/build-progress` and it reads the newest Gradle log, then shows:

- whether the build is **running**, **OK** or **FAILED**
- how many tasks have run so far
- the task it is on right now
- how long it has been running since its last log write
- the first five compile errors

It is meant for long Android builds (R8 release builds can take an hour on a phone), where you want to check on progress without scrolling a log.

## Install

In Claude Code:

```
/plugin marketplace add xUmutKx/claude-build-progress
/plugin install build-progress@xUmutKx
```

Or clone the repo and point Claude Code at the folder.

## Use

```
/build-progress                 # newest log in ./_logs, ./ or $BUILD_LOG_DIR
/build-progress path/to/log     # a specific log file
/build-progress path/to/folder  # newest log inside that folder
```

The plugin only reads log files. It never runs Gradle.

## Log format

It understands plain Gradle console output: `> Task :name` lines, `e:` compile errors and the `BUILD SUCCESSFUL` / `BUILD FAILED` line. If your wrapper script appends an `exit=N` line, that line decides OK or FAILED.

## Requirements

- Python 3 (standard library only)
- Claude Code with plugin support

## License

MIT
