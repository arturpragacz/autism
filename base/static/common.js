function notImplemented() {
	alert("Not implemented!");
}

$(function() {
	let params = new URLSearchParams(document.location.search);
	let v = params.get("q");
	$("#id_q").val(v === null ? "" : v);
});
