# Users Guide

This document is to explain use case with actual command line.
About the example, you can refer an integration test script [tests/integration/run.sh](../tests/integration/run.sh) test_foo method too.

For documentation on the recipe file format, see the [RHSCL Rebuild Recipes](https://github.com/sclorg/rhscl-rebuild-recipes).

## Architecture

The application is to help building a list of RPM packages.

And it is structured from several parts that are "Main application", "Recipe", "Download", "Build", "Work directory".

"Main" is a main application that will get "Recipe" data from recipe file for a defined list of the RPM packages and download and build them.

"Download" is how to get a list of building RPM packages.

"Build" is how to build the list of the RPM packages.

"Main" will order "Download" and "Build".

"Work directory" will manage working directory strucure. See below section for detail.


### Structured factors

```

Main --> Recipe (recipe file)
 |
 +-----> Download +-----> Get pacakges from local directory
 |                |
 |                +-----> Get pacakges from repository by fedpkg(or rhpkg) clone
 |                |
 |                +-----> Custom Download -> Define the behavior
 |                                           by the config file.
 |
 +-----> Build ---+-----> Mock Build
                  |
                  +-----> Copr Build
                  |
                  +-----> Koji Build
                  |
                  +-----> Custom Build -> Define the behavior
                                          by the config file.
```

### Relationship of Recipe file, Source directory and Work directory

#### Recipe file (ex. `ror50.yml`)

```
rh-ror50:
  packages:
    - rh-ror50:
        macros:
          install_scl: 0
    # Packages required by RSpec, Cucumber
    - rubygem-rspec
    - rubygem-rspec-core:
        replaced_macros:
          need_bootstrap_set: 1
    - rubygem-rspec-support:
        replaced_macros:
          need_bootstrap_set: 1
    - rubygem-diff-lcs:
        macros:
          _with_bootstrap: 1
```

#### Source directory

If you want to build from your packages on SOURCE_DIRECTORY in local environment. The SOURCE_DIRECTORY is like this. Just put the packages in same directory.

```
source_directory/
├── rh-ror50
│   ├── LICENSE
│   ├── README
│   ├── rh-ror50.spec
│   └── sources
├── rubygem-diff-lcs
│   ├── rubygem-diff-lcs.spec
│   └── sources
├── rubygem-rspec
│   ├── rubygem-rspec.spec
│   └── sources
├── rubygem-rspec-core
│   ├── rspec-core-3.5.4-Fixes-for-Ruby-2.4.patch
│   ├── rspec-related-create-full-tarball.sh
│   ├── rubygem-rspec-core.spec
│   └── sources
└── rubygem-rspec-support
    ├── rspec-related-create-full-tarball.sh
    ├── rubygem-rspec-support-3.2.1-callerfilter-searchpath-regex.patch
    ├── rubygem-rspec-support-3.6.0.beta2-fix-for-ruby-2.4.0.patch
    ├── rubygem-rspec-support-3.6.0.beta2-fix-for-ruby-2.4.0-tests.patch
    ├── rubygem-rspec-support.spec
    └── sources
```

#### Work directory

1. Application creates work directory to build. Each subdirectory has number directory that means the order of the build. The number directory name may be zero padding (`0..00N`) by considering the maxinum number of packages in the recipe file.

2. The application rename original spec file to `foo.spec.orig`, and create new file `foo.spec` that is editted to inject macros definition in the recipe file.

```
work_directory/
├── 1
│   └── rh-ror50
│       ├── LICENSE
│       ├── README
│       ├── rh-ror50.spec
│       ├── rh-ror50.spec.orig
│       └── sources
├── 2
│   └── rubygem-rspec
│       ├── rubygem-rspec.spec
│       ├── rubygem-rspec.spec.orig
│       └── sources
├── 3
│   └── rubygem-rspec-core
│       ├── rspec-core-3.5.4-Fixes-for-Ruby-2.4.patch
│       ├── rspec-related-create-full-tarball.sh
│       ├── rubygem-rspec-core.spec
│       ├── rubygem-rspec-core.spec.orig
│       └── sources
├── 4
│   └── rubygem-rspec-support
│       ├── rspec-related-create-full-tarball.sh
│       ├── rubygem-rspec-support-3.2.1-callerfilter-searchpath-regex.patch
│       ├── rubygem-rspec-support-3.6.0.beta2-fix-for-ruby-2.4.0.patch
│       ├── rubygem-rspec-support-3.6.0.beta2-fix-for-ruby-2.4.0-tests.patch
│       ├── rubygem-rspec-support.spec
│       ├── rubygem-rspec-support.spec.orig
│       └── sources
└── 5
    └── rubygem-diff-lcs
        ├── rubygem-diff-lcs.spec
        ├── rubygem-diff-lcs.spec.orig
        └── sources
```


## Tutorial

1. First of all, run below command to see the command help.

        $ rpmlb -h

2. Below is `rpmlb`'s basic form. You have to set proper download type, build type, recipe file, reicpe ID. If you omit `--download`, `--build`, the default values are used. You can also use short option name too. See the command help for more detail.

        $ rpmlb \
          --download DOWNLOAD_TYPE \
          --build BUILD_TYPE \
          RECIPE_FILE \
          COLLECTION_ID

### Select download type

#### Local

1. If you have not registered your pacakges to the respository yet, you may want to build from your pacakges on SOURCE_DIRECTORY in local environment. In the case, run

        $ rpmlb \
          --download local \
          --source-directory SOURCE_DIRECTORY \
          ...
          RECIPE_FILE \
          COLLECTION_ID

#### Fedpkg

1. If you have registered your packages to the repository, you may want to build from the packages in repository. In the case, run with `--branch`.

        $ rpmlb \
          --download fedpkg \
          --branch BRANCH \
          ...
          RECIPE_FILE \
          COLLECTION_ID

#### Rhpkg

1. If you want to use `rhpkg` instead of `fedpkg`, run with `--download rhpkg`. Other options are same with `--download fedpkg`.

        $ rpmlb \
          --download rhpkg \
          --branch BRANCH \
          ...
          RECIPE_FILE \
          COLLECTION_ID

#### Custom download

1. You may want to customize your download way. In case, you can run with `--custom-file`.

        $ rpmlb \
          ...
          --download custom \
          --custom-file CUSTOM_FILE \
          ...
          RECIPE_FILE \
          COLLECTION_ID

2. What is the custom file? See [sample custom files](../tests/fixtures/custom). It is YAML file like `.travis.yml`. You can write shell script in the file.

  * `before_download`: Write commands to run before build.
  * `download`: Write commands to run for each packages in the pacakges directory. You can use environment variable `PKG` to describe the package name.

For both hooks, the environment variable `CUSTOM_DIR` refers to the directory containing the custom file
(allowing configuration files and helper scripts to be located relative to it).

### Specify work directory

1. As a default behavior of the application creates work directory to `/tmp/rpmlb-XXXXXXXX`. However you want to specifiy the directory, run with `--work-directory`.

        $ rpmlb \
          ...
          --work-directory WORK_DIRECTORY \
          ...
          RECIPE_FILE \
          COLLECTION_ID

### Select build type

#### Mock build

1. If you wan to build with mock, run with `--mock-config` (it is same with `mock -r`).

        $ rpmlb \
          ...
          --build mock \
          --mock-config MOCK_CONFIG \
          ...
          RECIPE_FILE \
          COLLECTION_ID

#### Copr build

1. Prepare copr repo to build by yourself.
   The feature to create the copr repo by script is still not supported.

2. If you want to delete pacakages in the copr, run

        $ scripts/delete_copr_pkgs.sh COPR_REPO

3. To build for Copr, enter

        $ rpmlb \
          ...
          --build copr \
          --copr-repo COPR_REPO \
          ...
          RECIPE_FILE \
          COLLECTION_ID

#### Koji build

[Koji]: https://koji.fedoraproject.org/koji/
[CBS]: https://cbs.centos.org/koji/

1.  Ensure that you have configuration for the desired koji instance
    (i.e. [Fedora Koji][Koji], [CentOS CBS][CBS], …) installed on your system.

    *   If you are unsure, check that the file
        `/etc/koji.conf.d/<profile>.conf` exists.

2.  To build for any Koji instance, enter

        $ rpmlb
          ...
          --build koji \
          --koji-epel EPEL_VERSION \
          --koji-profile PROFILE \
          --koji-owner OWNER \
          ...
          RECIPE_FILE \
          COLLECTION_ID

    Here, `EPEL_VERSION` is the major EL version you wish to build for
    (i.e. `7` for CentOS 7), `PROFILE` names the configuration profile
    to use (it acts the same as `koji --profile` option) and `OWNER` is the
    name of the user that should own any new packages in the build target.

    You can also specify `--koji-scratch` flag to test your build(s).

    If the build target name does not follow the convention of [CBS][],
    where each target is named as `sclo{el}-{collection}-rh-el{el}`,
    you can override this template with the option `--koji-target-format`.
    Any `{el}`, `{collection}` placeholders will be replaced with
    the EL version and SCL name, respectively,
    when choosing a target to build into.

#### Custom build

1. You may want to customize your build way. In case, you can run with `--custom-file`.

        $ rpmlb \
          ...
          --build custom \
          --custom-file CUSTOM_FILE \
          ...
          RECIPE_FILE \
          COLLECTION_ID

2. What is the custom file? See [sample custom files](../tests/fixtures/custom). It is YAML file like `.travis.yml`. You can write shell script in the file.

  * `before_build`: Write commands to run before build.
  * `build`: Write commands to run for each packages in the pacakges directory. You can use environment variable `PKG` to describe the package name.

For both hooks, the environment variable `CUSTOM_DIR` refers to the directory containing the custom file
(allowing configuration files and helper scripts to be located relative to it).

#### Don't build

1. If you don't want to build, only want to download the pacakges to create work directory. and later want to build only. In case, run **without** `--build` or with `--build dummy`. Then you can see the log for the dummy build. This is good to check your recipe file.

        $ rpmlb \
          ...
          --build dummy \
          ...
          RECIPE_FILE \
          COLLECTION_ID

### Resume from any position of pacakges

1. If your build was failed during the process due to some reasons, you want to resume your build. In case run with `--work-directory` and  `--resume`. The resume number is same with the number directory name in work directory. zero padding is ignored. That is ex. 01 => 1, 012 => 12.

        $ rpmlb \
          ...
          --build BUILD_TYPE \
          --work-directory WORK_DIRECTORY \
          --resume 35 \
          ...
          RECIPE_FILE \
          COLLECTION_ID

### Specify retry count for build

1. You can set retry count for build. For example, below sample shows that the build is run 3 times after the 1st build failed. (= totally try to build 4 times.). When this retry option is not specified, retry count is zero. (retry is disabled.)

        $ rpmlb \
          ...
          --retry 3 \
          ...
          RECIPE_FILE \
          COLLECTION_ID

### Specify a package command explicitly

1. The package command `fedpkg` or `rhpkg` are used in build type: Mock, Copr. If you want to specify the command from command option, you can use `--cmd-pkg` option.

2. If `--download fedpkg or rhpkg` is specified, the package command is also used in the build.
3. If the download type is not `fedpkg`, and not `rhpkg`, `fedpkg` is used as a default.

        $ rpmlb \
          ...
          --download fedpkg \
          --build copr \
          --copr-repo COPR_REPO \
          --pkg-cmd rhpkg \
          ...
          RECIPE_FILE \
          COLLECTION_ID

### Specify a distribution mode

1.  You may want to build specified packages, edit RPM spec file or run `patch` command for specified distribution platform. In that case, you can set conditional `dist` element or environment variable `DIST` in the recipe file.

        $ rpmlb \
          ...
          --dist centos \
          ...
          RECIPE_FILE \
          COLLECTION_ID

2. We are supporting the values such as `fc`, `fc26`, `centos`, `centos7`, `el`, `el7` as a value of `--dist`.

### Recipe file, custom file and environment variables

1. You can use enviornment variables in a recipe file (`cmd` element) or custom file.

        $ FOO=foo BAR=bar rpmlb \
          ...
          RECIPE_FILE \
          COLLECTION_ID

2. Recipe file

        joke:
          name: Joke
          packages:
            - sl:
                cmd: echo "${FOO}"

3. Custom file

        build:
          - echo "${BAR}"
