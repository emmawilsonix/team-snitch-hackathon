import { Component, OnChanges } from '@angular/core';

@Component({
  selector: 'app-individual-leaderboard',
  templateUrl: './individual-leaderboard.component.html',
  styleUrls: ['./individual-leaderboard.component.scss']
})
export class IndividualLeaderboardComponent implements OnChanges {

  public listOfIndividuals = [{
    name: 'Kim Smith',
    team: 'Party Parrot',
    points: 110
  }, {
    name: 'Josh Butcher',
    team: 'Coffee Cat',
    points: 108
  }];

  constructor() { }

  ngOnChanges(): void {
  }

}
