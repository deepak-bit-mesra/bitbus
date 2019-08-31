
const listOfHolidays = ["Tue Jan 01 2019", "Tue Jan 15 2019", "Sat Jan 26 2019", "Sun Feb 10 2019", "Mon Mar 04 2019", "Thu Mar 21 2019", "Mon Apr 08 2019", "Sat Apr 13 2019", "Sun Apr 14 2019", "Wed Apr 17 2019", "Fri Apr 19 2019", "Sat May 18 2019", "Wed Jun 05 2019", "Thu Jul 04 2019", "Mon Aug 12 2019", "Thu Aug 15 2019", "Fri Aug 23 2019", "Mon Sep 09 2019", "Tue Sep 10 2019", "Tue Sep 17 2019", "Wed Oct 02 2019", "Sat Oct 05 2019", "Sun Oct 06 2019", "Mon Oct 07 2019", "Tue Oct 08 2019", "Sun Oct 27 2019", "Sat Nov 02 2019", "Sun Nov 10 2019", "Tue Nov 12 2019", "Fri Nov 15 2019", "Wed Dec 25 2019"];
const mon = "Mon-Fri";
const sun = "Sun";
const sat = "Sat";
const week = [sun,mon,mon,mon,mon,mon,sat];
var globalvariable = null;


var app = angular.module('myApp',[]);
app.controller('myCtrl',function($scope,$http){
    globalvariable = $scope;
    $scope.currDate = new Date();
    $scope.currTime = $scope.currDate;
    $scope.currTime.setSeconds(0,0);
    $scope.admin = {"source":"frombit","typeofbus":"All"}
    // setProperTime($scope.RoutineArr);
    const BIT = "BIT";
    const Ranchi = "Ranchi"
    $scope.travel = {source:BIT,destination:Ranchi};









    
    function fetchRecord(weekday,source){
        let arr = jQuery.grep(routine.res,
            function(element,index){
                return element.typeofday=== weekday;
            });
    }
    
    $scope.changeSource = function(ev){

        if($scope.travel.source==BIT)
            $scope.travel.destination = Ranchi
        if($scope.travel.source==Ranchi)
            $scope.travel.destination = BIT
    }

    $scope.changeDestination = function(){
        if($scope.travel.destination==BIT)
            $scope.travel.source = Ranchi
        if($scope.travel.destination==Ranchi)
            $scope.travel.source = BIT
    }
    
    $scope.adminBusSearch = function(ev){
        console.log("Source= ",$scope.admin.source);
        console.log("typeofbus = ",$scope.admin.typeofbus);
        $scope.adminResults = $scope.filter($scope.admin.source,$scope.admin.typeofbus,getWeekDay(null,new Date()));
        debugger;
    }

    $scope.setTime = function(){
        $scope.currTime.setMinutes(00,00,00)
    }


    

    $scope.fetchRoutine = function(){
        let config = {
            method:"GET",url:'/routine',headers:{"Content-Type":"application/json"},data:{}
        }
        $scope.routine = null;
        $http(config).then(function(response){
            globalvariable.routine = response.data.res;


            //Set Proper Week Day


            $scope.adminResults = $scope.filter($scope.admin.source,$scope.admin.typeofbus,getWeekDay(null,new Date()));
            console.group();
            console.log("suc",response);
            console.table(globalvariable.routine);
            console.groupEnd();
            
        },
        function(response){
            console.error("Error in Routine");
        });
    }

    $scope.filter = function(source,typeofbus,typeofday){
        let arr=[];
        for(x of globalvariable.routine){
            var obj={};
            if( x[source]!=null && (x["typeofbus"]==typeofbus ||typeofbus=="All") && x["typeofday"]==typeofday){ 
                obj.departure= x[source];
                obj.typeofbus = x["typeofbus"];
                obj.isCancelled = !x["isRunning"];//Do Not Ignore This
                obj.hasDeparted = x["hasdeparted"];
                obj.idtimetable = x["idtimetable"];
                obj.typeofday = x["typeofday"]
                arr.push(obj);
            }
        }
        return arr;
    }

    $scope.setStatus = function(isCancelled,hasDeparted,idtimetable){
        $scope.disable_hasDeparted = true;
        $scope.disable_isCancelled = true;
        let config = {
            url:"/ttRecordResource/"+idtimetable,
            method:"PUT",
            headers:{"Content-Type":"application/json"},
            data:{
                "idtimetable": idtimetable,
                "isRunning": !isCancelled,
                "hasdeparted": hasDeparted
            }
        }
        debugger;
        $http(config).then(function (response) {
            $scope.disable_hasDeparted = false;
            $scope.disable_isCancelled = false;
            console.log("response = ",response);
            debugger;
        },
        function(response){
            console.log(" fail response = ",response);
            $scope.disable_hasDeparted = false;
            $scope.disable_isCancelled = false;
            debugger;
        });
    }

    


    
});



function setProperTime(arr){//This FUnction is to Feed Data in HTML Input type= Date inn proper format
    for(i in arr){
        let hours,minutes,seconds=null;
        if(arr[i].departure!=null){
            [hours,minutes,seconds] = arr[i].departure.split(':');
            arr[i].departure = new Date(1970,0,1,hours,minutes,seconds);
        }


    }
}

function getWeekDay(idofDatePicker,dateObject){//Get weekDay from Current Date and Holiday
    if(idofDatePicker!=null) {   
        let dtVal = document.getElementById(idofDatePicker).value;
        if(listOfHolidays.indexOf(dtVal)!= -1)
            return "Sun";//Yes Its Holiday
        dt = new Date(dtVal);
        return week[dt.getDay()];
    }

    else if(dateObject!=null){
        let listOfHolidayss = listOfHolidays.map(x=> (new Date(x)).getTime());
        dateObject.setHours(0,0,0,0);//Since the List has hours as 0;
        if (listOfHolidayss.indexOf(dateObject.getTime()) != -1)
            return sun;//Holiday from calendar
        return week[dateObject.getDay()];
        
    }
}
const compareDate=(date1,date2)=>{
    return date1.getTime() === date2.getTime();
}
function getDate(){
    var today = new Date();

    document.getElementById("date").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);


}
