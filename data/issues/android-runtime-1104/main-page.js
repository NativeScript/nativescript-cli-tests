function onNavigatingTo(args) {
    var page = args.object;
    console.log("### TEST START ###");
    com.tns.mylib.Log();
    sleep(2000);
    console.log("### TEST SHOULD NOT CRASH ###");
    console.log("### TEST END ###");
}
exports.onNavigatingTo = onNavigatingTo;

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}