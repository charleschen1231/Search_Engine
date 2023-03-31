/* add click event listener to result urls */
let resultUrls = document.getElementsByClassName('result-url');
for (let i = 0; i < resultUrls.length; i++) {
    resultUrls[i].addEventListener('click', function() {
        let url = this.getAttribute('href');
        window.open(url, '_blank');
    });
}

/* add click event listener to pagination links */
let pageLinks = document.getElementsByClassName('page-link');
for (let i = 0; i < pageLinks.length; i++) {
    pageLinks[i].addEventListener('click', function() {
        let url = this.getAttribute('href');
        window.location.href = url;
    });
}
