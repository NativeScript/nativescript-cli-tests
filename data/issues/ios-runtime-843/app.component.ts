import { Component } from "@angular/core";

@Component({
    selector: "ns-app",
    templateUrl: "app/app.component.html",
})
export class AppComponent {
    constructor() {
        console.log("Hey App!");
        console.time("startup");
        setTimeout(() => {
            console.timeEnd("startup");
        }, 1000);
    }
 }
