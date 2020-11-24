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
  private usersList: IUser[];

  constructor(
    private apiService: LeaderboardApiService,
  ) {}

  ngOnInit(): void {
    // Note: Remove these from here when we have actual data
    // Get test users for now
    this.getTestTeams();
    this.getTestUsers();
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

  /** Function to get test users */
  public getTestUsers(): void {
    this.apiService
      .getAllTestUsers()
      .subscribe(response => {
        this.usersList = this.parseUsers(response);
      },
      console.error
    );
  }

  /** Function to make first and last name title-case */
  public titleCaseName(name: string) {
    const titleCasedName = name.charAt(0).toUpperCase() + name.substring(1);
    return titleCasedName;
 }

 /** Function to parse users and get names from emails */
  public parseUsers(users: IUser[]): IUser[] {
    users.forEach(user => {
      let fullName: string[]  = user.emailAddress.split('@');
      fullName = fullName[0].split('.');
      const firstName: string = this.titleCaseName(fullName[0]);
      const lastName: string = this.titleCaseName(fullName[1]);
      const fullNameString: string = firstName + ' ' + lastName;
      user.name = fullNameString;
    });
    return users;
  }
}
