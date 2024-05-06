
# TuxSuite Component

## Introduction

TuxSuite Component facilitates a complete CI/CD pipeline specifically for building and testing the Linux Kernel tree on QEMU environments. This component is part of the larger TuxSuite ecosystem, provided by Linaro, which supports Linux kernel development with a suite of tools and services.

## Getting Started

### Prerequisites

- A Linux Kernel tree hosted on a gitlab instance.
- Access to modify CI/CD settings in your Git repository.

### Configuration

1. **Integrate with your CI/CD pipeline:**

   To use the TuxSuite Component with your Linux kernel project, add the reference kernel pipeline YAML file to your project. This can be done by setting the CI/CD configuration in your project settings(Settings -> CI/CD -> "CI/CD configuration file"):

   ```plaintext
   .gitlab-ci-kernel.yml@Linaro/components/tuxsuite
   ```

   Reference YAML file: [.gitlab-ci-kernel.yml](https://gitlab.com/Linaro/components/tuxsuite/-/raw/test/.gitlab-ci-kernel.yml?ref_type=heads)

   Set the timeout value for the pipeline to 6h since the some builds and test run for longer duration. The timeout needs to be adjusted if the jobs timeout. This can be done by setting the CI/CD configuration in your project settings(Settings -> CI/CD -> General Pipelines -> Timeout)

2. **Submit Custom TuxSuite Plan:**
   The default [TuxSuite Plan](https://docs.tuxsuite.com/plan/kernel/) that is run on the kernel is [here](https://gitlab.com/Linaro/components/tuxsuite/-/blob/test/templates/boot/plan.yml?ref_type=heads). It builds the kernel and runs ltp-smoke test on QEMU using gcc compiler for these architecture: armv5, armv7, arm64, i386, mips, powerpc, riscv, sparc and x86_64.

   The user can choose to host their own TuxSuite Plan covering the tests suitable for their usecase and pass it to the pipeline. We will pass a TuxSuite Plan to run tc-testing during git push as shown below:

   ```plaintext
   git push -o ci.variable="PLAN=https://gitlab.com/Linaro/tuxsuite/-/raw/master/examples/kselftest-tc-testing-test.yaml?ref_type=heads"
   ```

3. **Supported Toolchains, QEMU Targets and Tests:**

   - [Supported Architectures](https://tuxmake.org/architectures/)
   - [Supported Toolchains](https://tuxmake.org/toolchains/)
   - [Supported QEMU Targets](https://tuxrun.org/devices/#qemu-devices)
   - [Supported Tests](https://tuxrun.org/tests/#qemu-devices)


4. **(Optional) Use TuxSuite cloud to do the builds and testing on DUTs:**

   Users can choose to use TuxSuite Cloud which provides much more support than the tuxsuite local execution. The benefits of TuxSuite cloud is listed [here](https://learn.tuxsuite.com/features/). The list of DUTs available via TuxSuite Cloud is [here](https://docs.tuxsuite.com/tuxtest/real-hardware-testing/#supported-real-hardwares).

   - To use TuxSuite Cloud which supports extensive testing on large set of real DUTs, you need to request a TuxSuite TOKEN [here](https://docs.google.com/forms/d/e/1FAIpQLSdbYpVhYphuqD25nkZzx8vYlkLGib63Q9vADBd9-10iUNkHjQ/viewform).
   - Add your TuxSuite Token as a CI/CD Variables (Settings-> CI/CD -> Variables -> Add variable). Add "TUXUITE_TOKEN" in the key field and <Generated TOKEN> in the value field.
   - Please unselect "Protect variable" checkbox and select "Mask variable" checkbox.

5. **GitLab Minutes to run CI/CD Pipelines**

   **On https://gitlab.com, Please fork the linux kernel from Gitlab backed Linux kernel Tree from [here](https://gitlab.com/linux-kernel/linux)**

   Gitlab provides around 400 free Gitlab minutes for CI/CD pipelines. Gitlab provides additional minutes on forks of Gitlab backed Open Source project. The users get additional minutes by forking their development tree from the above kernel tree.

   Additional details about discounted CI/CD minutes can be found [here](https://docs.gitlab.com/ee/ci/pipelines/cicd_minutes.html#cost-factor)


### Tools Overview

- **[TuxSuite](https://docs.tuxsuite.com):** A CLI tool to run kernel builds and tests either locally or remotely in the cloud using tuxmake for building and tuxrun for testing.
- **[TuxMake](https://tuxmake.org):** A CLI and Python library that supports building the Linux kernel in various configurations and environments.
- **[TuxRun](https://tuxrun.org):** A CLI tool for testing Linux on QEMU and ARM FVP modules using curated test suites.

## Support

For issues, feedback, or contributions regarding TuxSuite Component, please visit [TuxSuite's Gitlab repository](https://gitlab.com/Linaro/tuxsuite).

## License

Copyright 2024 Linaro Limited

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.