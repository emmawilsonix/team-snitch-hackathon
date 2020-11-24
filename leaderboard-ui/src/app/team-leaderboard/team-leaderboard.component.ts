import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-team-leaderboard',
  templateUrl: './team-leaderboard.component.html',
  styleUrls: ['./team-leaderboard.component.scss']
})
export class TeamLeaderboardComponent implements OnInit {

  public houseStanding = [{
    teamID: 1,
    name: "Party Parrot",
    points: 2710,
    colour: "rgb(30, 149, 166)",
    img: "assets/images/parrot.png"
  },
  {
    teamID: 2,
    name: "Coffee Cat",
    points: 2599,
    colour: "rgb(135, 74, 162)",
    img: "assets/images/cat.png"
  },
  {
    teamID: 3,
    name: "Dancing Banana",
    points: 2404,
    colour: "rgb(217, 169, 0)",
    img: "assets/images/banana.png"
  },
  {
    teamID: 4,
    name: "Yay Orange",
    points: 2289,
    colour: "rgb(64, 150, 70)",
    img: "assets/images/orange.png"
  }]

  constructor() { }

  ngOnInit(): void {
  }

  // Placeholder
  public getHouseStanding(): void {
    console.log("Do something Eventually")
  }

}