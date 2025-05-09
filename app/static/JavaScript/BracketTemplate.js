const brackets =[
    {
        winner: {
            round1: {
                match1: {
                    player1: 'Player A',
                    player2: 'Player B',
                    team1: 'Team A',
                    team2: 'Team B',
                    score1: 3,
                    score2: 2,
                    winner: this.score1 > this.score2 ? 'Player A' : 'Player B',
                },
                match2: {
                    player1: 'Player C',
                    player2: 'Player D',
                    team1: 'Team C',
                    team2: 'Team D',
                    score1: 1,
                    score2: 4,
                    winner: this.score1 > this.score2 ? 'Player C' : 'Player D',
                },
                match3: {
                    player1: 'Player E',
                    player2: 'Player F',
                    team1: 'Team E',
                    team2: 'Team F',
                    score1: 5,
                    score2: 0,
                    winner: this.score1 > this.score2 ? 'Player E' : 'Player F',
                },
                match4: {
                    player1: 'Player G',
                    player2: 'Player H',
                    team1: 'Team G',
                    team2: 'Team H',
                    score1: 2,
                    score2: 3,
                    winner: this.score1 > this.score2 ? 'Player G' : 'Player H',
                },
            },
            round2: {
                match13: {
                    player1: 'Player A',
                    player2: 'Player C',
                    team1: 'Team A',
                    team2: 'Team C',
                    score1: 3,
                    score2: 2,
                    winner: this.score1 > this.score2 ? 'Player A' : 'Player C',
                },
                match14: {
                    player1: 'Player E',
                    player2: 'Player G',
                    team1: 'Team E',
                    team2: 'Team G',
                    score1: 1,
                    score2: 4,
                    winner: this.score1 > this.score2 ? 'Player E' : 'Player G',
                },
            },
            round3: {
                match19: {
                    player1: 'Player A',
                    player2: 'Player E',
                    team1: 'Team A',
                    team2: 'Team E',
                    score1: 1,
                    score2: 4,
                    winner: this.score1 > this.score2 ? 'Player A' : 'Player E',
                }
            },
            round4: {
                match23: {
                    player1: 'Player A',
                    player2: 'Player I',
                    team1: 'Team A',
                    team2: 'Team I',
                    score1: 1,
                    score2: 4,
                    winner: this.score1 > this.score2 ? 'Player A' : 'Player I',
                }
            }
        },
        loser: {
            round1: {
                match5: {
                    player1: 'Player I',
                    player2: 'Player J',
                    team1: 'Team I',
                    team2: 'Team J',
                    score1: 4,
                    score2: 1,
                    winner: this.score1 > this.score2 ? 'Player I' : 'Player J',
                },
                match6: {
                    player1: 'Player K',
                    player2: 'Player L',
                    team1: 'Team K',
                    team2: 'Team L',
                    score1: 0,
                    score2: 5,
                    winner: this.score1 > this.score2 ? 'Player K' : 'Player L',
                },
                match7: {
                    player1: 'Player M',
                    player2: 'Player N',
                    team1: 'Team M',
                    team2: 'Team N',
                    score1: 3,
                    score2: 3,
                    winner: this.score1 > this.score2 ? 'Player M' : 'Player N',
                },
                match8: {
                    player1: 'Player O',
                    player2: 'Player P',
                    team1: 'Team O',
                    team2: 'Team P',
                    score1: 2,
                    score2: 4,
                    winner: this.score1 > this.score2 ? 'Player O' : 'Player P',
                },
            },
            round2: {
                match9: {
                    player1: 'Player I',
                    player2: 'Player B',
                    team1: 'Team I',
                    team2: 'Team B',
                    score1: 4,
                    score2: 1,
                    winner: this.score1 > this.score2 ? 'Player I' : 'Player B',
                },
                match10: {
                    player1: 'Player K',
                    player2: 'Player D',
                    team1: 'Team K',
                    team2: 'Team D',
                    score1: 0,
                    score2: 5,
                    winner: this.score1 > this.score2 ? 'Player K' : 'Player D',
                },
                match11: {
                    player1: 'Player M',
                    player2: 'Player F',
                    team1: 'Team M',
                    team2: 'Team F',
                    score1: 3,
                    score2: 3,
                    winner: this.score1 > this.score2 ? 'Player M' : 'Player F',
                },
                match12: {
                    player1: 'Player O',
                    player2: 'Player H',
                    team1: 'Team O',
                    team2: 'Team H',
                    score1: 2,
                    score2: 4,
                    winner: this.score1 > this.score2 ? 'Player O' : 'Player H',
                },
            },
            round3: {
                match15: {
                    player1: 'Player I',
                    player2: 'Player K',
                    team1: 'Team I',
                    team2: 'Team K',
                    score1: 4,
                    score2: 1,
                    winner: this.score1 > this.score2 ? 'Player I' : 'Player K',
                },
                match16: {
                    player1: 'Player M',
                    player2: 'Player O',
                    team1: 'Team M',
                    team2: 'Team O',
                    score1: 0,
                    score2: 5,
                    winner: this.score1 > this.score2 ? 'Player M' : 'Player O',
                },
            },
            round4: {
                match17: {
                    player1: 'Player I',
                    player2: 'Player C',
                    team1: 'Team I',
                    team2: 'Team C',
                    score1: 4,
                    score2: 1,
                    winner: this.score1 > this.score2 ? 'Player I' : 'Player C',
                },
                match18: {
                    player1: 'Player M',
                    player2: 'Player E',
                    team1: 'Team M',
                    team2: 'Team E',
                    score1: 0,
                    score2: 5,
                    winner: this.score1 > this.score2 ? 'Player M' : 'Player E',
                },
            },
            round5: {
                match20: {
                    player1: 'Player I',
                    player2: 'Player M',
                    team1: 'Team I',
                    team2: 'Team M',
                    score1: 4,
                    score2: 1,
                    winner: this.score1 > this.score2 ? 'Player I' : 'Player M',
                },
            },
            round6: {
                match21: {
                    player1: 'Player I',
                    player2: 'Player E',
                    team1: 'Team I',
                    team2: 'Team E',
                    score1: 4,
                    score2: 1,
                    winner: this.score1 > this.score2 ? 'Player I' : 'Player E',
                }
            }
        },
    },
    // ...more records...
];

document.addEventListener('DOMContentLoaded', () => {
    // 1. Directly retrieve the <template> element from the DOM
    const tpl = document.getElementById('bracket-template').content;
    const clone = tpl.cloneNode(true);

    const match = (brackets[0])[0];
    console.log("bracket", brackets);
    Object.keys(brackets).forEach((competition) => {
        console.log("comp", brackets[competition]);
        Object.keys(brackets[competition]).forEach((matchKey, i) => {
            console.log("matchKey", brackets[competition][matchKey]);
            console.log("winner", brackets[competition][matchKey].winner);
        });

    });
    // 5. Fill main content
    Object.keys(brackets).forEach((competition) => {
        Object.keys(brackets[competition]).forEach((matchKey, i) => {
            const match = brackets[competition][matchKey];
            const p1MatchElement = clone.querySelector(`.match${i + 1}-player1`);
            p1MatchElement.querySelector('.player_name').textContent = match.player1;
            console.log("player1", match.player1);
            p1MatchElement.querySelector('.player_team').textContent = match.team1;
            p1MatchElement.querySelector('.score').textContent = match.score1;


            const p2MatchElement = clone.querySelector(`.match${i + 1}-player2`);
            p2MatchElement.querySelector('.player_name').textContent = match.player2;
            p2MatchElement.querySelector('.player_team').textContent = match.team2;
            p2MatchElement.querySelector('.score').textContent = match.score2;
        });

        document.getElementById('bracket-container').appendChild(clone);

    });
});