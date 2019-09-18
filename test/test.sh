EDDIR=/mnt/PASSPORT/data/eap/energy-dashboard
LOGLEVEL=INFO
PREFIX="--log-level ${LOGLEVEL}"
TESTFEED="abc-test-01"
#set -x

runcmd(){
    echo "-------------------------------------------------"
    echo $1
    echo "-------------------------------------------------"
    $1
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
    echo ""
    echo ""
}

#TEMPDIR=$(mktemp -d)
#pushd ${TEMPDIR}
mkdir ./data
runcmd pwd
runcmd "edc"
runcmd "edc --help"
runcmd "edc --ed-dir ${EDDIR} --help"
runcmd "edc ${PREFIX} license"
runcmd "edc ${PREFIX} feeds"
runcmd "edc ${PREFIX} feeds list"
runcmd "edc ${PREFIX} feed"
# may run against already created feed for speed
#runcmd_ignore_errors "edc ${PREFIX} feed ${TESTFEED} create -sdy 2019 -sdm 9 -sdd 1 --url=http://zwrob.com/assets/oasis_SZ_q_AS_MILEAGE_CALC_anc_type_ALL_sdt__START_T07_00-0000_edt__END_T07_00-0000_v_1.zip"
runcmd "edc ${PREFIX} feed ${TESTFEED} create -sdy 2019 -sdm 9 -sdd 1 --url=http://zwrob.com/assets/oasis_SZ_q_AS_MILEAGE_CALC_anc_type_ALL_sdt__START_T07_00-0000_edt__END_T07_00-0000_v_1.zip"
runcmd "edc ${PREFIX} feed ${TESTFEED} manifest show"
runcmd "edc ${PREFIX} feed ${TESTFEED} invoke \"ls\""
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
# if takes too long to download, comment out. TODO: need to fix test
runcmd "edc ${PREFIX} feed ${TESTFEED} proc download"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc unzip"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc parse"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc insert"
runcmd_ignore_errors "edc ${PREFIX} feed ${TESTFEED} proc save"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
runcmd "edc ${PREFIX} feed ${TESTFEED} archive"
#popd
#runcmd "edc ${PREFIX} feed ${TESTFEED} reset parse"

echo "TEST PASSED"
