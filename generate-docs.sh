wrap(){
    header=$1
    cmd=$2
    echo "$header"
    echo ""
    echo "\`\`\`bash"
    $cmd
    echo "\`\`\`"
    echo ""
}


wrap "## edc" "edc"
wrap "### config" "edc config"
wrap "### feed" "edc feed"
wrap "### feeds" "edc feeds"
wrap "### license" "edc license"

