import { Component, OnInit } from '@angular/core';
import { IUser, ITeam } from '../models/models';
import { LeaderboardApiService } from '../services/leaderboard-api.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {
  private teamsList: ITeam[];

  constructor(
    private apiService: LeaderboardApiService,
  ) {}

  ngOnInit(): void {
    // Note: Remove these from here when we have actual data
    // Get test users for now
    this.getTestTeams();
  }

  /** Function to get test teams */
  public getTestTeams(): void {
    this.apiService
      .getAllTestTeams()
      .subscribe(response => {
        this.teamsList = response;
      },
      console.error
    );
  }
}
