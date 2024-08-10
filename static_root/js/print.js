function printOut(divId) {
  var printOutContent = document.getElementById(divId).innerHTML;
  var originalContent = document.body.innerHTML;
  document.body.innerHTML = printOutContent;
  window.print();
  document.body.innerHTML = originalContent;
}
