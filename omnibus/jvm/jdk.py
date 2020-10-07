import os.path
import re
import sys
import typing as ta


OSX_PLATFORM = 'darwin'
OSX_JDK_PATH = '/Library/Java/JavaVirtualMachines'


def find_java_home() -> ta.Optional[str]:
    if sys.platform != OSX_PLATFORM:
        return None
    if not (os.path.exists(OSX_JDK_PATH) and os.path.isdir(OSX_JDK_PATH)):
        return None
    jdk_minor_home_pairs = [
        (int(match.groupdict()['minor']), home)
        for item in os.listdir(OSX_JDK_PATH)
        for full_path in [os.path.join(OSX_JDK_PATH, item)]
        if os.path.isdir(full_path)
        for match in [re.fullmatch(r'jdk1\.8\.0_(?P<minor>[0-9]+)\.jdk', item)]
        if match
        for home in [os.path.join(full_path, 'Contents', 'Home')]
        if os.path.exists(home) and os.path.isdir(home)
    ]
    if not jdk_minor_home_pairs:
        return None
    return sorted(jdk_minor_home_pairs, key=lambda t: -t[0])[0][1]
