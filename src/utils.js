function getVariables() {
    var _GET = {};
    if(document.location.toString().indexOf('?') !== -1) {
        var query = document.location
                      .toString()
                      // get the query string
                      .replace(/^.*?\?/, '')
                      // and remove any existing hash string (thanks, @vrijdenker)
                      .replace(/#.*$/, '')
                      .split('&');

        for(var i=0, l=query.length; i<l; i++) {
          var aux = decodeURIComponent(query[i]).split('=');
          _GET[aux[0]] = aux[1];
        }
    }
    return _GET;
}