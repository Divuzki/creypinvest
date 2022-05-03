// COPY TO CLIPBOARD
function copyToClipboard(text) {
  const elem = document.createElement("textarea");
  let timer;
  clearTimeout(timer);
  elem.value = text;
  document.body.appendChild(elem);
  elem.select();
  document.execCommand("copy");
  document.body.removeChild(elem);
  navigator.clipboard.writeText(text);
  var cpd_btn = document.getElementById("copyed_btn");
  if (cpd_btn) {
    cpd_btn.classList.add("copy_btn-copyed");
    cpd_btn.innerHTML = "<b>copyed</b>";
    timer = setTimeout(() => {
      cpd_btn.innerHTML = "<b>copy</b>";
      cpd_btn.classList.remove("copy_btn-copyed");
    }, 5000);
  } else alert("Copyed To Clipboard ✅");
}

function btcConversion(bitcoin) {
  var btcConvertValue = document.getElementsByClassName("convert-value-btc");
  if (btcConvertValue) {
    for (var key in btcConvertValue) {
      var dollars = btcConvertValue[key].getAttribute("data-btc-value");
      btcConvertValue[key].innerHTML = `₿${(dollars / bitcoin + 0.0005).toFixed(6)}`;
    }
  }
}

function btcPrice(bitcoin) {
  var BitcoinValue = document.getElementById("btc-value");
  if (BitcoinValue) {
    BitcoinValue.innerHTML = bitcoin;
  }
}
// BTC HTTP REQUEST FOR PRICE
window.onload = function () {

  // BTC CURRENT PRICE
  var bitcoinPrice = new XMLHttpRequest();
  bitcoinPrice.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      btcPrice(JSON.parse(this.responseText).DISPLAY.BTC.USD.PRICE);
      btcConversion(JSON.parse(this.responseText).RAW.BTC.USD.PRICE);
    }
  };
  bitcoinPrice.open(
    "GET",
    "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD",
    true
  );
  bitcoinPrice.send();
};
