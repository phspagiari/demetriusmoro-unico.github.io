function edit_url() {
    const base_repo = 'demetriusmoro-unico.github.io/';
    const url_prefix = 'https://github.com/demetriusmoro-unico/';
    const button_class = 'md-content__button md-icon'
    const base_url = String(
        document.getElementsByClassName(button_class)[0].href
    ).split('//')[1];
    
    const external = base_url.startsWith('doc/')
    var edit_url = base_url
    var edit_chunk = ''
    
    if (external) {
        edit_url = edit_url.substring(4, edit_url.length)
        edit_chunk = 'edit/main/mkdocs/doc/'
    }
    else {
        edit_url = base_repo + edit_url
        edit_chunk = 'edit/main/mkdocs/docs/'
    }
    
    const repo_chunk = edit_url.split('/')[0] + '/';
    edit_url = edit_url.replace(repo_chunk, repo_chunk + edit_chunk)

    window.open(url_prefix + edit_url);
}
