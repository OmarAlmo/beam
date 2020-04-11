function processRelevance(data,fid,docID, query){
	event.preventDefault();
	formID = "relevanceForm".concat(fid);
	successAlert = "successAlert".concat(fid);

	const xhr = new XMLHttpRequest()

	tmp = [data, docID, query]
	xhr.open('POST','/relevance')
	xhr.send(tmp)

	document.getElementById(formID).style.display="none";
	document.getElementById(successAlert).style.display="block";
}

