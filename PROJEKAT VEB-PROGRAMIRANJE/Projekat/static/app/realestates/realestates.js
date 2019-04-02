(function (angular) {
    var app = angular.module("Aplikacija");

   
    app.controller("NekretnineCtrl", function ($http) {

        var ln = this;

        ln.nekretnine= [];

        ln.dodajBool = false;

      
        ln.novi = {
            "title": "",
            "location": "",
            "price": "",
            "other_info": "",
            "image_src": ""
        };

        ln.zaIzmenu = {};

        ln.nekretnina = {}

        ln.dobaviNekretnine = function() {
         
            $http.get("/realestate").then(function(response) {
                ln.nekretnine = response.data;
            }, function(reason) {
                console.log(reason);
            });
        }

        ln.dodaj = function() {
            $http.post("/realestate", ln.novi).then(function(response){
                if(response.data["status"] == "done") {
                    ln.dobaviNekretnine();
                    ln.novi.title = null;
                    ln.novi.price = null;
                    ln.novi.other_info = null;
                    ln.novi.image_src = null;
                    ln.novi.location = null;
                }
            },
            function(reason){
                console.log(reason);
            })
        };

        ln.dobaviNekretninu = function(id) {
            $http.get("/realestate/"+id).then(function(response){
                ln.nekretnina = response.data;
            },
            function(reason){
                console.log(reason)
            });
        };

        ln.ukloni = function(id) {
            $http.delete("/realestate/"+id).then(function(response){
                ln.dobaviNekretnine();
            },
            function(reason){
                console.log(reason)
            });
        };

        ln.pripremiZaIzmenu = function(nekretnina) {
            ln.zaIzmenu = angular.copy(nekretnina);
        }

        ln.odustaniOdIzmene = function() {
            ln.zaIzmenu = {};
        }

        ln.izmeniNekretninu = function() {
            $http.put("/realestate/"+ln.zaIzmenu.id, ln.zaIzmenu).then(function(response){
                ln.dobaviNekretnine();
                ln.zaIzmenu = {};
            },
            function(reason){
                console.log(reason)
            });
        }

        ln.dobaviNekretnine();
    });
})(angular);