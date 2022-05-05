/*
Author: Creyp Invest Inc.
*/

(function () {
  //===== Prealoder

    var btcConvertValue = document.getElementsByClassName("convert-value-btc");
    
  // Btc Converter 
  function btcConversion(bitcoin) {
    if (btcConvertValue) {
      for (var key in btcConvertValue) {
        var dollars = btcConvertValue[key].getAttribute("data-btc-value");
        btcConvertValue[key].innerHTML = `${(
          dollars / bitcoin +
          0.0005
        ).toFixed(6)}`;
      }
    }
  }
  window.onload = function () {
    window.setTimeout(fadeout, 500);
    if (btcConvertValue) {
      // BTC CURRENT PRICE
      var bitcoinPrice = new XMLHttpRequest();
      bitcoinPrice.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
          btcConversion(JSON.parse(this.responseText).RAW.BTC.USD.PRICE);
        }
      };
      bitcoinPrice.open(
        "GET",
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD",
        true
      );
      bitcoinPrice.send();
    }
  };

  function fadeout() {
    document.querySelector(".preloader").style.opacity = "0";
    document.querySelector(".preloader").style.display = "none";
  }

  /*=====================================
    Sticky
    ======================================= */
  window.onscroll = function () {
    var header_navbar = document.querySelector(".navbar-area");
    var sticky = header_navbar.offsetTop;

    var logo = document.querySelector(".navbar-brand img");
    if (window.pageYOffset > sticky) {
      header_navbar.classList.add("sticky");
      logo.src =
        "https://dp2qyyzsg7qig.cloudfront.net/static/images/logo/logo.svg";
    } else {
      header_navbar.classList.remove("sticky");
      logo.src =
        "https://dp2qyyzsg7qig.cloudfront.net/static/images/logo/white-logo.svg";
    }

    // show or hide the back-top-top button
    var backToTo = document.querySelector(".scroll-top");
    if (
      document.body.scrollTop > 50 ||
      document.documentElement.scrollTop > 50
    ) {
      backToTo.style.display = "flex";
    } else {
      backToTo.style.display = "none";
    }
  };

  // WOW active
  new WOW().init();

  //===== mobile-menu-btn
  let navbarToggler = document.querySelector(".mobile-menu-btn");
  navbarToggler.addEventListener("click", function () {
    navbarToggler.classList.toggle("active");
  });
})();
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
