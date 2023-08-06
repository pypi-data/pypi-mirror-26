#!/bin/bash -x

show_usage() {
    CMD=$(basename "${0}")
    cat <<EOF
Usage: ${CMD} COPR_REPO
EOF
}

quit_program() {
    echo "You pressed Ctrl-C. Quit the program."
    exit 1
}

# Enable trapping Ctrl-C for the safety.
trap quit_program INT

if [ ${#} -lt 1 ]; then
    show_usage
    exit 1
fi

# See https://copr.fedorainfracloud.org/coprs/USER/COPR_REPO
COPR_REPO="${1}"
COPR_CLI='copr-cli'

PKG_NAMES="$("${COPR_CLI}" list-package-names "${COPR_REPO}")"

for PKG_NAME in ${PKG_NAMES}; do
    "${COPR_CLI}" delete-package --name "${PKG_NAME}" "${COPR_REPO}"
done
