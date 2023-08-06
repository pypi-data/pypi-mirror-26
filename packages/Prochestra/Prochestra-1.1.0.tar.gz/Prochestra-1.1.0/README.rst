Prochestra
==========

*Prochetra* is a small Python module for calling a set of processes
with dependencies in a series.

It is meant to be used for assembling a set of process calls into one single call.
A process call can have a number of dependencies. In a way, that it will not be executed
if one of its dependencies failed, or exited with return code other than 0, respectively.
The return code of *Procestra* is 0, if every subprocess call returned 0; otherwise it is 1.

The output of all processes is written to the ``stdout``, one single logfile, or dismissed.

The process calls and its dependencies are defined in a JSON or YAML file.

Usage
-----

A definition for three process calls with one dependency relationship could look like this::

    jobs:
    - id: j1
      cmd: "batchjob1"
      args: ["-c" "/usr/local/etc/someconfig"]
    - id: j2
      cmd: "batchjob2"
    - id: j3
      cmd: "batchjob3"
      dependencies:
      - j1

The processes are called in the given order. The jobs ``j1`` and ``j2`` are executed no matter what.
But, job ``j3`` is executed only, if the job ``j1`` returned with exit code 0.

To run the job list, saved as ``jobs.yaml``, put ``prochestra``, or ``prochestra.cmd``, respectively, on the ``PATH`` and run::

    prochestra jobs.yaml

To find out all possible command line arguments for *Prochestra*, print the help text like this::

    prochestra --help

License
-------

This project is released under the MIT license.

Copyright |copy| 2017 by Tobias Kiertscher <dev@mastersign.de>.

.. |copy| unicode:: U+000A9 .. COPYRIGHT SIGN