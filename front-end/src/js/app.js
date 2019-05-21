var my_app = new Vue({
    el: '#app',
    data: {
      ajaxRequest: false,
      markers: [],
      my_points: [],
      shared_to_me: [],
      info: {"name": null},
      note: 8,
      close: false,
      surname: null,
      pointadd: true,
      sig_id: '',
      key: ''
    },
    watch: {
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
      removediv: function(){
        console.log("ok");
      },
      loaddata: function(){
        var infowindow = new google.maps.InfoWindow;
        this.markers.forEach(function(e){
          e.setMap(null)
        });
        for (var i = 0; i < this.my_points.length; i++){
          var icon = {
            url: "../assets/img/float.svg",
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
                 my_app.info = { "name":  my_app.my_points[i].name, "surname":  my_app.my_points[i].surname }
             }
          })(this.markers[i], i));
          this.markers[i].setMap(map);
        }
        for (; i < this.my_points.length + this.shared_to_me.length; i++){
          var icon = {
            url: "../assets/img/floatred.png",
            scaledSize: new google.maps.Size(40, 40)
          }
          var myLatlng = new google.maps.LatLng(48.813896,2.392448);
          this.markers[i] = new google.maps.Marker({
            position: myLatlng,
            title:"Hello World!",
            icon: icon
          });
          this.markers[i].setMap(map);
        }

        if(i == 0)
          this.pointadd = true
        else {
          this.pointadd = false
        }
        console.log(this.pointadd)
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
        url = "http://51.75.30.103/addpoint/"
        axios.post(url, data)
             .then(response => {
               console.log(data)
               this.fetchdata()
            }).catch(error => console.log(error));
        this.key = ''
        this.sig_id = ''
      },
      rename: function(){
        this.ajaxRequest = true;
        if (this.surname == null)
          return;
        data = {
          "mail": this.mail,
          "token": this.token,
          "surname": this.surname
        }
        url = "http://51.75.30.103/surname/"
        axios.post(url, data)
             .then(response => {
               this.fetchdata()
            }).catch(error => console.log(error));
        this.surname = null
      },
      fetchdata: function() {
        this.ajaxRequest = true;
        data = {
          "mail": this.mail,
          "token": this.token
        }
        url = "http://51.75.30.103/allinfos/"
        axios.post(url, data)
             .then(response => {
               ret = response["data"]["data"]
               this.my_points = ret["my_points"]
               this.shared_to_me = ret["shared_to_me"]
                 console.log(this.my_points)
                 this.loaddata()
            }).catch(err => {});
      }
    },
    mounted(){
       if (localStorage.mail == void 0 || localStorage.token == void 0) {
         window.location.href = "login.html";
       } else {
         this.mail = localStorage.mail
         this.token = localStorage.token
         this.fetchdata()
       }
    }
})
