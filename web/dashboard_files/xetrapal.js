var serverip = "192.168.56.101"
var xetrapal={
  load_dashboard: function(){
    xetrapal.get_api_status()
    xetrapal.get_api_profile()
    xetrapal.get_smriti_status()
    setInterval(function(){
      xetrapal.get_api_status()
      xetrapal.get_api_profile()
      xetrapal.get_smriti_status()
    },15000);
  },
  get_api_status: function(){
    console.log("Fetching API status")
    $.getJSON("http://"+serverip+":5000/", function(data){
      //console.log(data)
      $("#api_status").html(data.resp[0].replace(/\n/g,"<br>"))
    })

  },
  get_api_profile: function(){
    console.log("Fetching API profile")
    $.getJSON("http://"+serverip+":5000/api_profile", function(data){
      //console.log(data)
      $("#api_profile").html(JSON.stringify(data.resp[0]))
    })
  },
  get_smriti_status: function(){
    console.log("Fetching Smriti status")
    $.getJSON("http://"+serverip+":5000/smriti_status", function(data){
      //console.log(data)
      $("#smriti_status").html(JSON.stringify(data.resp[0]))
    })
  },
}
