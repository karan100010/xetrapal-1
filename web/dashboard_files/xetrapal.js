var serverip = "192.168.56.101"
var xetrapal={
  load_dashboard: function(){
    xetrapal.get_api_status()
    xetrapal.get_api_profile()
    xetrapal.get_smriti_status()
  },
  get_api_status: function(){
    console.log("Fetching API status")
    setInterval(function(){
      $.getJSON("http://"+serverip+":5000/", function(data){
        //console.log(data)
        $("#api_status").html(data.resp[0].replace(/\n/g,"<br>"))
      })
    },3000);
  },
  get_api_profile: function(){
    console.log("Fetching API profile")
    setInterval(function(){
      $.getJSON("http://"+serverip+":5000/api_profile", function(data){
        //console.log(data)
        $("#api_profile").html(JSON.stringify(data.resp[0]))
      })
    },3000);
  },
  get_smriti_status: function(){
    console.log("Fetching Smriti status")
    setInterval(function(){
      $.getJSON("http://"+serverip+":5000/smriti_status", function(data){
        //console.log(data)
        $("#smriti_status").html(JSON.stringify(data.resp[0]))
      })
    },3000);
  },
}
