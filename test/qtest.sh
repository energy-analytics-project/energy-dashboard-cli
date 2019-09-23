EDDIR=/mnt/PASSPORT/data/eap/energy-dashboard
LOGLEVEL=INFO
#LOGLEVEL=DEBUG
PREFIX="--log-level ${LOGLEVEL}"
TESTFEED="abc-test-01"
RESULT=""
#set -x

runcmd(){
    echo "-------------------------------------------------"
    echo $1
    echo "-------------------------------------------------"
    RESULT="$($1)"
    echo "${RESULT}"
    if [ "$?" != "0" ]; then
        echo "TEST FAILED!!!"
        exit 1
    fi
    echo ""
    echo ""
}

runcmd_ignore_errors(){
    echo "-------------------------------------------------"
    echo $1
    echo "-------------------------------------------------"
    RESULT="$($1)"
    echo "${RESULT}"
    echo ""
    echo ""
}

rm -rf ./data
mkdir ./data
runcmd pwd

runcmd "edc"
runcmd "edc --help"
runcmd "edc --ed-dir ${EDDIR} --help"
runcmd "edc ${PREFIX} license"
runcmd "edc ${PREFIX} feeds"
runcmd "edc ${PREFIX} feeds list"
runcmd "edc ${PREFIX} feed"
runcmd "edc ${PREFIX} feed ${TESTFEED} create -sdy 2019 -sdm 9 -sdd 1 --url=http://zwrob.com/assets/oasis_SZ_q_AS_MILEAGE_CALC_anc_type_ALL_sdt__START_T07_00-0000_edt__END_T07_00-0000_v_1.zip"
runcmd "edc ${PREFIX} feed ${TESTFEED} manifest show"
runcmd "edc ${PREFIX} feed ${TESTFEED} invoke \"ls\""
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"

# no need to download, that code is simple and slows down tests
# runcmd "edc ${PREFIX} feed ${TESTFEED} proc download"
mkdirs -p ./data/${TESTFEED}/zip
cp -rv testdata/zip/* ./data/${TESTFEED}/zip/.

runcmd "edc ${PREFIX} feed ${TESTFEED} reset unzip --no-confirm"
runcmd "edc ${PREFIX} feed ${TESTFEED} reset parse --no-confirm"
runcmd "edc ${PREFIX} feed ${TESTFEED} reset insert --no-confirm"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc unzip"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc parse"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc insert"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
runcmd_ignore_errors "edc ${PREFIX} feed ${TESTFEED} proc save"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
runcmd "edc ${PREFIX} feed ${TESTFEED} archive"
ARCHIVE=${RESULT}
runcmd "edc ${PREFIX} feed ${TESTFEED} reset unzip --no-confirm"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
rm -rf ./data/${TESTFEED}
runcmd "edc ${PREFIX} feed ${TESTFEED} restore ${ARCHIVE}"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"

echo "QUICK TEST PASSED"
