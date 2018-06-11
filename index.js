var config = {
  apiKey: "AIzaSyBZZ_DWPh7fjkpdO7-bqvuoOTvRaEPPN3Q",
  authDomain: "gpumonitor-d6f94.firebaseapp.com",
  databaseURL: "https://gpumonitor-d6f94.firebaseio.com",
  projectId: "gpumonitor-d6f94",
  storageBucket: "gpumonitor-d6f94.appspot.com",
  messagingSenderId: "1006877681656"
};

Vue.component("monitorctn",{
  template:'#cardInfoContainer',
  props: ["info"],
  computed: {
    styleobj: function() {
      return {transform: "rotate("+ this.info.Utilization * 1.8+"deg)"};
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
        for(keyindex in keys){
          var server = gpudata[keys[keyindex]].GPU;
          var GPUs = server.map(function(e,gpuindex){
            e.server = keys[keyindex];
            e.index = gpuindex;
            return e;
          });
          infos = infos.concat(GPUs);
        }
      return infos;
    }
  }
})