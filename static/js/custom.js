// to get current year
function getYear() {
  var currentDate = new Date();
  var currentYear = currentDate.getFullYear();
  document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// owl.owlcarousel2_filter

$(".owl-filter-bar").on("click", ".item", function (e) {
  var $items = $(".owl-filter-bar a");
  var $item = $(this);
  var filter = $item.data("owl-filter");
  $items.removeClass("active");
  $item.addClass("active");
  owl.owlcarousel2_filter(filter);

  e.preventDefault();
});

$("#pin").on("change", function () {
  var max = parseInt($(this).attr("max"));
  var min = parseInt($(this).attr("min"));
  if ($(this).val() > max) {
    $(this).val(max);
  } else if ($(this).val() < min) {
    $(this).val(min);
  }
});

// timer
// Set the date we're counting down to
var days = 11;
var date = new Date("2022-07-24");
var countDownDate = new Date(date.getTime() + days * 24 * 60 * 60 * 1000);
// Update the count down every 1 second
if (document.getElementById("countDay")) {
  var x = setInterval(function () {
    // Get today's date and time
    var now = new Date().getTime();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    // Output the result in an element with id="demo"
    document.getElementById("countDay").innerHTML = days;

    document.getElementById("countHour").innerHTML = hours;

    document.getElementById("countMin").innerHTML = minutes;

    document.getElementById("countSec").innerHTML = seconds;

    // If the count down is over, write some text
    if (distance < 0) {
      clearInterval(x);
      document.getElementById("countDay").innerHTML = "EXPIRED";
    }
  }, 1000);
}

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

// BTC LIVE
function clearBTCGraph(resText) {
  var dates = [];
  var bitcoinPrice = [];
  for (var key in resText) {
    var date = new Date(key);
    dates.push(
      date.getDate() + "/" + date.getMonth() + "/" + date.getFullYear()
    );
    bitcoinPrice.push(resText[key]);
  }
  console.log(dates);
  var ctx = document.getElementById("valueBitcoinChart");
  if (ctx) {
    ctx.getContext("2d");
    var myChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: dates,
        datasets: [
          {
            label: "Value Of Bitcoin (USD)",
            backgroundColor: "rgba(163, 205, 147, 0.3)",
            borderColor: "#64b443",
            data: bitcoinPrice,
          },
        ],
      },
    });
  }
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

function btcChange(value) {
  var BitcoinConditionValue = document.getElementsByClassName("btc-condition");
  if (BitcoinConditionValue) {
    for (var key in BitcoinConditionValue) {
      if (value < 0 && BitcoinConditionValue[key])
        BitcoinConditionValue[key].classList.add("neg");
      else BitcoinConditionValue[key].classList.remove("neg");
      BitcoinConditionValue[key].innerHTML = `${value.toFixed(2)}%`;
    }
  }
}

// BTC HTTP REQUEST FOR MARKET SUMMARY
window.onload = function () {
  // BTC YEARLY HISTORY
  var bitcoinHistorical = new XMLHttpRequest();
  bitcoinHistorical.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      clearBTCGraph(JSON.parse(this.responseText).bpi);
    }
  };
  bitcoinHistorical.open(
    "GET",
    "https://api.coindesk.com/v1/bpi/historical/close.json?index=USD",
    true
  );
  bitcoinHistorical.send();

  // BTC MARKET CHANGE
  var bitcoinChange = new XMLHttpRequest();
  bitcoinChange.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      btcChange(JSON.parse(this.responseText).data.BTC.change.percent);
    }
  };
  bitcoinChange.open(
    "GET",
    "https://production.api.coindesk.com/v2/tb/price/ticker?assets=BTC",
    true
  );
  bitcoinChange.send();

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

  // WEBLOADER
  var webLoaderOverlay = document.querySelector(".creyp-loader-overlay");
  var webLoader = document.querySelector(".creyp-loader");
};
