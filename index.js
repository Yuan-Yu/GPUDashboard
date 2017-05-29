var data_url =  'https://gpumonitor-d6f94.firebaseio.com/Servers.json?print=pretty';
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
    myfirst: { transform: 'rotate(10deg)'},
    infos:[]
  },mounted: function(){
    var vobj = this;
    var loadDATA=function() {
        axios.get(data_url).then(function (response){ 
        var keys = Object.keys(response.data);
        var infos = [];
        for(keyindex in keys){
          var server = response.data[keys[keyindex]].GPU;
          var GPUs = server.map(function(e,gpuindex){
            e.server = keys[keyindex];
            e.index = gpuindex;
            return e;
          });
          infos = infos.concat(GPUs);
        }
        vobj.infos = infos;
      });
    }
    loadDATA();
    window.setInterval(loadDATA,5000);
  }
})