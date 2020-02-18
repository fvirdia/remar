# -*- coding: utf-8 -*-

import subprocess
import asyncio


async def run(cmd, cwd=None):
    """Run rMAPI in a subshell and return stdout.
    Adapted from the basic example at https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process.communicate

    :param cmd:     rMAPI commmand
    :param cwd:     system directory to run rmpai from
    """
    print("> %s" % cmd)
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd)

    stdout, _ = await proc.communicate()
    return stdout.decode()


class rMAPIException(Exception):
    pass


class rMAPIWrapper:

    def __init__(self, binary="rmapi"):
        self.busy = False
        self.binary = binary

    def set_binary(self, binary):
        self.binary = binary

    async def run_command(self, cmd, cwd=None):
        """Spans a rMAPI process to run a command and captrue its output.

        :param cmd:     rMAPI commmand
        :param cwd:     system directory to run rmpai from
        """
        if self.busy:
            raise rMAPIException("Busy contacting server.")

        self.busy = True
        ret = await run("%s %s" % (self.binary, cmd), cwd=cwd)
        self.busy = False
        return ret

    async def ls(self, directory="", cb=None):
        """Lists documents in a directory.

        :param directory:   directory to list the content of
        :param cb:          callback after directory content is obtained
        """
        ret = await self.run_command("ls \"%s\"" % directory)

        out = ret.split("\n")[1:-1]
        directories = []
        files = []
        for entry in out:
            kind, filename = entry.split('\t')
            if kind == "[d]":
                directories.append(filename)
            elif kind == "[f]":
                files.append(filename)
            else:
                raise ValueError("Unexpected kind of entry in %s: %s" % (directory, entry))
        directories.sort()
        files.sort()

        if cb:
            cb(directories, files)
        return directories, files

    async def put(self, path, directory="", cb=None):
        """Uploads document in a directory.

        :param path:        path of the document to upload
        :param directory:   directory to upload to
        :param cb:          callback after documenti s uploaded
        """
        await self.run_command("put \"%s\" \"%s\"" % (path, directory))
        if cb:
            cb(path)

    async def geta(self, path, directory=None, cb=None):
        ret = await self.run_command("geta \"%s\"" % (path), cwd=directory)
        if cb:
            cb(path, directory)
