#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_installer, build_shared
import os

if __name__ == "__main__":

    arch = os.getenv("ARCH", "x86_64")
    builder = build_template_installer.get_builder()
    settings = {"os": build_shared.get_os(), "arch_build": arch, "arch": arch}
    if "MINGW_CONFIGURATIONS" in os.environ:
        configs = os.environ["MINGW_CONFIGURATIONS"]
        for config in configs.split(","):
            tokens = config.strip().split('@')
            settings["compiler"] = "gcc"
            settings["compiler.version"] = tokens[0]
            settings["arch"] = tokens[1]
            settings["compiler.exception"] = tokens[2]
            settings["compiler.threads"] = tokens[3]
            settings["compiler.libcxx"] = "libstdc++"
            build_requires = {"*": ["mingw-w64/8.1"]}
            builder.add(settings, {}, {}, build_requires)
    else:
        builder.add(settings, {}, {}, {})
    builder.run()
