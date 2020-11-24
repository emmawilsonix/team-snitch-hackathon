export interface ITeam {
    teamID: number;
    name: string;
    team_points: number;
    colour?: string;
    img?: string;
}

export interface IUser {
    userID: number;
    teamID: number;
    emailAddress: string;
    points: number;
    name?: string;
    teamName?: string;
}

export interface ITeamStyles {
    colour: string;
    image: string;
}

export interface ITeamNameMappings {
    [id: number]: string;
}

export interface ITeamStylesMappings {
    [id: number]: ITeamStyles;
}
