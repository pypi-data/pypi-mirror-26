Prochestra
==========

.. image:: https://img.shields.io/pypi/format/prochestra.png
   :target: https://pypi.python.org/pypi/Prochestra

.. image:: https://img.shields.io/github/release/mastersign/prochestra.png
   :target: https://github.com/mastersign/prochestra/releases

*Prochestra* is a small Python module for calling a set of processes
with inter-dependencies in a series.
It is meant to be used for assembling a set of process calls into one single call, e.g. in a cronjob.

A process call can have a number of dependencies. In a way, that it will not be executed,
if one of its dependencies failed, or exited with return code other than 0, respectively.
The return code of *Prochestra* is 0, if every subprocess call returned 0; otherwise it is 1.

The output of all processes is written to the ``stdout``, one single logfile, or dismissed.

The process calls and its dependencies are defined in a JSON or YAML file.

Installation
------------

*Prochestra* is published on PyPI::

    pip install prochestra

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

To run the job list, saved as ``jobs.yaml``, run::

    prochestra jobs.yaml

To find out all possible command line arguments for *Prochestra*, print the help text like this::

    prochestra --help

Alternative Usage
-----------------

If you download the project directly instead of using PIP for installation,
you can run the scripts ``bin/prochestra`` (Bash) or ``bin\prochestra.cmd`` (Windows CMD) directly,
or put ``bin`` on your ``PATH``.

Another alternative is to run *Prochestra*  as a module::

    python -m prochestra myjobs.json

And finally you can use the classes ``JobList`` and ``Prochestra`` from the ``prochestra`` module
in your own Python code if you want to dynamically generate job lists::

    from prochestra import Prochestra, JobList

    job_list = {'jobs': [
        {'id': 'j1', 'cmd': 'python', 'args': ['-c', 'print("Hello World 1"); exit(1)']},
        {'id': 'j2', 'cmd': 'python', 'args': ['-c', 'print("Hello World 2")'], 'dependencies': ['j1']},
        {'id': 'j3', 'cmd': 'python', 'args': ['-c', 'print("Hello World 3")']},
      ]}
    runner = Prochestra()
    result = runner.run(JobList(job_list))
    if not result:
        print('At least one process failed.')

License
-------

This project is released under the MIT license.

Copyright |copy| 2017 by Tobias Kiertscher <dev@mastersign.de>.

.. |copy| unicode:: U+000A9 .. COPYRIGHT SIGN
