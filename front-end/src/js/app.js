var my_app = new Vue({
    el: '#app',
    data: {
      mail: '',
      ajaxRequest: false,
      markers: [],
      my_points: [],
      shared_to_me: [],
      info: {"name": null},
      note: 8,
      close: false,
      surname: '',
      pointadd: false,
      sig_id: '',
      key: '',
      share: false,
      point_id_share: 0,
      error: "",
      mail_to_share: "",
      closesec: false,
      pointstat: false,
      api: "https://eliotctl.fr/api/wellcheck/"
    },
    watch: {
      point_id_share: function(){
        console.log("test")
      },
      info: function(){
        this.note = this.getnote(this.info.datas)
      }
    },
    filters: {
      sub : function(str, max) {
        res = str.substring(0,max);
        if (res != str) {
            res += "..."
        }
        return res;
      }
    },
    methods: {
      getnote: function(data){
        if  (data.length == 0) {
          return 'NaN'
        }
        data = data[0]
        pt = 0
        pt += data.turbidity <= 100 ? 2.5 : 0
        pt += data.conductance <= 100 ? 1.5 : 0
        pt += data.ph <= 8.2 && data.ph >= 6.5 ? 4 : 0
        pt += data.temperature <= 200 ? 2 : 0
        return pt
      },
      loaddata: function(){
        var infowindow = new google.maps.InfoWindow;
        this.markers.forEach(function(e){
          e.setMap(null)
        });
        localStorage.my_point = this.my_points
        localStorage.shared_to_me = this.shared_to_me

        for (var i = 0; i < this.my_points.length; i++){
          var icon = {
            url: "https://eliotctl.fr/WellCheck/assets/img/float.png",
            scaledSize: new google.maps.Size(40, 40)
          }
          var myLatlng = new google.maps.LatLng(this.my_points[i].location.lat,this.my_points[i].location.lng);
          this.markers[i] = new google.maps.Marker({
            position: myLatlng,
            title:this.my_points[i].surname,
            icon: icon
          });
          google.maps.event.addListener(this.markers[i], 'click', (function(marker, i) {
             return function() {
                 my_app.info = { "id": my_app.my_points[i].id,"datas": my_app.my_points[i].data, "name":  my_app.my_points[i].name, "surname":  my_app.my_points[i].surname, "status": ' proprietaire ('+my_app.mail+')'}
             }
          })(this.markers[i], i));
          this.markers[i].setMap(map);
        }
        for (; i < this.my_points.length + this.shared_to_me.length; i++){
          var icon = {
            url: "https://eliotctl.fr/WellCheck/assets/img/floatred.png",
            scaledSize: new google.maps.Size(40, 40)
          }
          j = i - this.my_points.length
          var myLatlng = new google.maps.LatLng(this.shared_to_me[j].location.lat, this.shared_to_me[j].location.lng);
          this.markers[i] = new google.maps.Marker({
            position: myLatlng,
            title:this.shared_to_me[j].surname,
            icon: icon
          });
          google.maps.event.addListener(this.markers[i], 'click', (function(marker, j) {
             return function() {
                 my_app.info = { "id": my_app.shared_to_me[j].id, "datas": my_app.shared_to_me[j].data, "name":  my_app.shared_to_me[j].name, "surname":  my_app.shared_to_me[j].surname, "status": " partagé (" +my_app.shared_to_me[j].sharefrom[0]+")" }
             }
          })(this.markers[i], j));
          this.markers[i].setMap(map);
        }

        if(i == 0)
          this.pointadd = true
        else {
          this.pointadd = false
        }
      },
      setuperror: function(error){
        this.error = '<div class="alert alert-danger alert-dismissible" style="text-align: center;" role="alert" ><button type="button" v-click="error = \"\"" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><i class="fa fa-times-circle" style="margin-right: 10px;"></i>   Error : ' + error + '</div>'
      },
      addpoint: function(){
        this.ajaxRequest = true;
        if (this.key == '' || this.sig_id == '')
          return;
        data = {
          "mail": this.mail,
          "token": this.token,
          "key": this.key,
          "sig_id": this.sig_id
        }
        url = this.api + "addpoint/"
        axios.post(url, data)
             .then(response => {
               if (response["data"]["error"] != void 0)
                  return this.setuperror(response["data"]["error"])
               this.fetchdata()
            }).catch(error => {console.log(error)});
        this.key = ''
        this.sig_id = ''
        this.pointadd = false
      },
      sharepoint: function(){
        this.ajaxRequest = true;
        if (this.point_id_share == 0 || this.mail_to_share == '')
          return;
        data = {
          "mail": this.mail,
          "token": this.token,
          "mail_to": this.mail_to_share,
          "point_id": this.point_id_share
        }
        url = this.api + "share/"
        axios.post(url, data)
             .then(response => {
               if (response["data"]["error"] != void 0)
                  return this.setuperror(response["data"]["error"])
               this.fetchdata()
            }).catch(error => {console.log(error)});
        this.mail_to_share = ''
        this.point_id_share = 0
        this.share = false
        this.info.surname = null
      },
      rename: function(){
        this.ajaxRequest = true;
        if (this.surname == '')
          return;
        console.log(this.info.id)
        data = {
          "mail": this.mail,
          "token": this.token,
          "surname": this.surname,
          "point_id": this.info.id
        }
        url = this.api + "surname/"
        axios.post(url, data)
             .then(response => {
               if (response["data"]["error"] != void 0)
                  return this.setuperror(response["data"]["error"])
               this.fetchdata()
            }).catch(error => {console.log(error)});
        this.surname = ''
        this.close = false
        this.pointstat = false
      },
      fetchdata: function() {
        this.ajaxRequest = true;
        data = {
          "mail": this.mail,
          "token": this.token
        }
        url = this.api + "allinfos/"
        axios.post(url, data)
             .then(response => {
               if (response["data"]["error"] != void 0)
                  return this.setuperror(response["data"]["error"])
               ret = response["data"]["data"]
               this.my_points = ret["my_points"]
               this.shared_to_me = ret["shared_to_me"]
               this.loaddata()
            }).catch(error => {console.log(error)});
      }
    },
    mounted(){
       if (localStorage.mail == void 0 || localStorage.token == void 0) {
         window.location.href = "login.html";
       } else {
         this.mail = localStorage.mail
         this.token = localStorage.token
         this.my_points = localStorage.my_point != void 0 ? localStorage.my_point : this.my_points
         this.shared_to_me = localStorage.shared_to_me != void 0 ? localStorage.shared_to_me : this.my_points
         this.fetchdata()
       }

    }
})
