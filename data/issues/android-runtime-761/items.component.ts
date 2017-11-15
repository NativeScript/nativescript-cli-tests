import { Component, OnInit, ViewChild, ElementRef } from "@angular/core";
var appSettings = require("application-settings");
var application = require('application');
var utils = require("utils/utils");
declare var android:any;

import { Item } from "./item";
import { ItemService } from "./item.service";

@Component({
    selector: "ns-items",
    moduleId: module.id,
    templateUrl: "./items.component.html",
})
export class ItemsComponent implements OnInit {

    private appContext;

    constructor() {
        var that = this;
        this.appContext = application.android.context;

        if(application.android){
            var telListener = android.telephony.PhoneStateListener.extend({
                onCallStateChanged: function (state:number, incomingNumber:string){
                    console.log(state);
                     switch(state) {
                        case android.telephony.TelephonyManager.CALL_STATE_OFFHOOK:
                        case android.telephony.TelephonyManager.CALL_STATE_RINGING:
                            console.log("call is coming");
                           
                    }
                }
            });

            var TelephonyMgr = this.appContext.getSystemService(android.content.Context.TELEPHONY_SERVICE);
            TelephonyMgr.listen(new telListener(), android.telephony.PhoneStateListener.LISTEN_CALL_STATE);
        }
    }

    ngOnInit(): void {      
    }

    
}
