var config = {
      apiKey: "XXXXXXXXXXXXXXXXXXXXXXXXXX",
      authDomain: "XXXXX.firebaseapp.com",
      databaseURL: "https://XXXXXXX.firebaseio.com",
      projectId: "XXXXX",
      storageBucket: "",
      messagingSenderId: "XXXXX"
    };
    
var levelColors = {'safe':'#8ac442','warning':'#f9bb0d','danger':'#fc1046'}
var timeCutoff = 5 * 60 * 1000; // cutoff in millisecond

Vue.component("monitorctn",{
  template:'#cardInfoContainer',
  props: ["info"],
  computed: {
    styleobj: function() {
      return {transform: "rotate("+ this.info.Utilization * 1.8+"deg)"};
    },
    memusageStyle: function(){
      var color = this.setColor(this.info.MemoryUsage);
      return {width: 150*0.01*this.info.MemoryUsage+"px",backgroundColor:color};
    },
    freeMem: function(){
      return "Free Memory: "+this.info.MemoryFree+" MB"
    },utilizationStyle(){
      var color = this.setColor(this.info.Utilization);
      return {backgroundColor:color}
    },clockspeed(){
      return "Current clock speed: "+this.info.Clock+" MHz"
    }
  },methods:{
    setColor(percent){
      var color;
      if(percent>=90){
        color = levelColors['danger'];
      }else if(percent>=80){
        color = levelColors['warning'];
      }else{
        color = levelColors['safe'];
      }
      return color;
    }
  }
});
var monitor = new Vue({
  el: '#monitor',
  data: {
    infos:[]
  },mounted: function(){
    var vobj = this;
    var gpufire = firebase.initializeApp(config);
    var database = gpufire.database();
    var ref = database.ref('Servers');
    ref.on('value',(snapshot)=>{
      vobj.infos = vobj.rearrageData(snapshot.val());
    });
  },methods:{
    rearrageData(gpudata){
        var keys = Object.keys(gpudata);
        var infos = [];
        var now = new Date(Date.now());
        for(keyindex in keys){
          var server = gpudata[keys[keyindex]].GPU;
          var GPUs = Object.values(server)
          .sort((GPU1,GPU2)=>{return (GPU1.GPUID>GPU2.GPUID)?1:-1;})
          .map(function(e){
            var logDate = new Date(e.logDateTime);
            e.server = keys[keyindex];
            e.disconnect =( Math.abs(now - logDate) > timeCutoff)? true:false;
            return e;
          });
          infos = infos.concat(GPUs);
        }
      return infos;
    }
  }
})