function getCorpus(){
    return document.getElementById('corpus').value
}

function showResult(q) {
    const xhr = new XMLHttpRequest()
    const corpus = getCorpus()
    
    event.preventDefault();

    qlen = q.split(" ").length;
    if (qlen >= 5){
        tmp = [q,corpus];
        console.log(q, corpus)
        xhr.open('POST','/autocomplete');
        xhr.send(tmp);
    

    // res = xhr.open('GET', '/autocomplete', true);
    // console.log(res)
    }

    // availableTags = xhr.open('GET', '/autocomplete', true);
    // $( "#searchbar" ).autocomplete({
    //     source: availableTags
    // });
}