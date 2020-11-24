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
    img?: string;
}

export interface ITeamStyles {
    colour: string;
    image: string;
}

export interface ITeamImageStyles {
    img: string;
    height: string;
    width: string;
}
export interface ITeamNameMappings {
    [id: number]: string;
}

export interface ITeamImgMappings {
    [id: number]: ITeamImageStyles;
}

export interface ITeamStylesMappings {
    [id: number]: ITeamStyles;
}
