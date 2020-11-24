import { Component, OnInit } from '@angular/core';
import { ITeam, ITeamStylesMappings } from '../models/models';
import { LeaderboardApiService } from '../services/leaderboard-api.service';

@Component({
  selector: 'app-team-leaderboard',
  templateUrl: './team-leaderboard.component.html',
  styleUrls: ['./team-leaderboard.component.scss']
})
export class TeamLeaderboardComponent implements OnInit {

  public teamsList: ITeam[];
  private teamStyleMappings: ITeamStylesMappings = {
    1: {
      colour: 'rgb(30, 149, 166)',
      image: 'assets/images/parrot.png'
    },
    2: {
      colour: 'rgb(135, 74, 162)',
      image: 'assets/images/cat.png'
    },
    3: {
      colour: 'rgb(217, 169, 0)',
      image: 'assets/images/banana.png'
    },
    4: {
      colour: 'rgb(64, 150, 70)',
      image: 'assets/images/orange.png'
    },
    // Placeholder
    5: {
      colour: 'rgb(64, 150, 70)',
      image: 'assets/images/orange.png'
    }
  };

  constructor(private apiService: LeaderboardApiService) { }

  ngOnInit(): void {
    this.getTestTeams();
  }

  /** Function to get test teams */
  public getTestTeams(): void {
    this.apiService
      .getAllTestTeams()
      .subscribe(response => {
        response.forEach(team => {
          team.colour = this.teamStyleMappings[team.teamID].colour;
          team.img = this.teamStyleMappings[team.teamID].image;
        });
        this.teamsList = response.splice(0,4).sort((a, b) => (b.team_points) - (a.team_points));
      },
      console.error
    );
  }
}