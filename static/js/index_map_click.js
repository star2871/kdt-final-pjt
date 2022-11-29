var countryElements = document.getElementById("countries").childNodes;
var countryCount = countryElements.length;
for (var i = 0; i < countryCount; i++) {
  countryElements[i].onclick = function () {
    location.href = this.getAttribute("data-id");
  };
}
