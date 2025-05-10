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
                    winner: function() { return (this.score1 > this.score2) ? 'Player A' : 'Player B'; },
                },
                match2: {
                    player1: 'Player C',
                    player2: 'Player D',
                    team1: 'Team C',
                    team2: 'Team D',
                    score1: 1,
                    score2: 4,
                    winner: function() { return (this.score1 > this.score2) ? 'Player C' : 'Player D'; },
                },
                match3: {
                    player1: 'Player E',
                    player2: 'Player F',
                    team1: 'Team E',
                    team2: 'Team F',
                    score1: 5,
                    score2: 0,
                    winner: function() { return (this.score1 > this.score2) ? 'Player E' : 'Player F'; },
                },
                match4: {
                    player1: 'Player G',
                    player2: 'Player H',
                    team1: 'Team G',
                    team2: 'Team H',
                    score1: 2,
                    score2: 3,
                    winner: function() { return (this.score1 > this.score2) ? 'Player G' : 'Player H'; },
                },
            },
            round2: {
                match1: {
                    player1: 'Player A',
                    player2: 'Player C',
                    team1: 'Team A',
                    team2: 'Team C',
                    score1: 3,
                    score2: 2,
                    winner: function() { return (this.score1 > this.score2) ? 'Player A' : 'Player C'; },
                },
                match2: {
                    player1: 'Player E',
                    player2: 'Player G',
                    team1: 'Team E',
                    team2: 'Team G',
                    score1: 1,
                    score2: 4,
                    winner: function() { return (this.score1 > this.score2) ? 'Player E' : 'Player G'; },
                },
            },
            round3: {
                match1: {
                    player1: 'Player A',
                    player2: 'Player E',
                    team1: 'Team A',
                    team2: 'Team E',
                    score1: 1,
                    score2: 4,
                    winner: function() { return (this.score1 > this.score2) ? 'Player A' : 'Player E'; },
                },
            },
            round4: {
                match1: {
                    player1: 'Player A',
                    player2: 'Player I',
                    team1: 'Team A',
                    team2: 'Team I',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player A' : 'Player I'; },
                },
            },
        },
        loser: {
            round1: {
                match1: {
                    player1: 'Player I',
                    player2: 'Player J',
                    team1: 'Team I',
                    team2: 'Team J',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player I' : 'Player J'; },
                },
                match2: {
                    player1: 'Player K',
                    player2: 'Player L',
                    team1: 'Team K',
                    team2: 'Team L',
                    score1: 0,
                    score2: 5,
                    winner: function() { return (this.score1 > this.score2) ? 'Player K' : 'Player L'; },
                },
                match3: {
                    player1: 'Player M',
                    player2: 'Player N',
                    team1: 'Team M',
                    team2: 'Team N',
                    score1: 3,
                    score2: 3,
                    winner: function() { return (this.score1 < this.score2) ? 'Player M' : 'Player N'; },
                },
                match4: {
                    player1: 'Player O',
                    player2: 'Player P',
                    team1: 'Team O',
                    team2: 'Team P',
                    score1: 2,
                    score2: 4,
                    winner: function() { return (this.score1 > this.score2) ? 'Player O' : 'Player P'; },
                },
            },
            round2: {
                match1: {
                    player1: 'Player I',
                    player2: 'Player B',
                    team1: 'Team I',
                    team2: 'Team B',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player I' : 'Player B'; },
                },
                match2:{
                    player1: 'Player K',
                    player2: 'Player D',
                    team1: 'Team K',
                    team2: 'Team D',
                    score1: 0,
                    score2: 5,
                    winner: function() { return (this.score1 > this.score2) ? 'Player K' : 'Player D'; },
                },
                match3: {
                    player1: 'Player M',
                    player2: 'Player F',
                    team1: 'Team M',
                    team2: 'Team F',
                    score1: 3,
                    score2: 3,
                    winner: function() { return (this.score1 > this.score2) ? 'Player M' : 'Player F'; },
                },
                match4: {
                    player1: 'Player O',
                    player2: 'Player H',
                    team1: 'Team O',
                    team2: 'Team H',
                    score1: 2,
                    score2: 4,
                    winner: function() { return (this.score1 > this.score2) ? 'Player O' : 'Player H'; },
                },
            },
            round3: {
                match1: {
                    player1: 'Player I',
                    player2: 'Player K',
                    team1: 'Team I',
                    team2: 'Team K',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player I' : 'Player K'; },
                },
                match2: {
                    player1: 'Player M',
                    player2: 'Player O',
                    team1: 'Team M',
                    team2: 'Team O',
                    score1: 0,
                    score2: 5,
                    winner: function() { return (this.score1 > this.score2) ? 'Player M' : 'Player O'; },
                },
            },
            round4: {
                match1: {
                    player1: 'Player I',
                    player2: 'Player C',
                    team1: 'Team I',
                    team2: 'Team C',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player I' : 'Player C'; },
                },
                match2: {
                    player1: 'Player M',
                    player2: 'Player E',
                    team1: 'Team M',
                    team2: 'Team E',
                    score1: 0,
                    score2: 5,
                    winner: function() { return (this.score1 > this.score2) ? 'Player M' : 'Player E'; },
                },
            },
            round5: {
                match1: {
                    player1: 'Player I',
                    player2: 'Player M',
                    team1: 'Team I',
                    team2: 'Team M',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player I' : 'Player M'; },
                },
            },
            round6: {
                match1: {
                    player1: 'Player I',
                    player2: 'Player E',
                    team1: 'Team I',
                    team2: 'Team E',
                    score1: 4,
                    score2: 1,
                    winner: function() { return (this.score1 > this.score2) ? 'Player I' : 'Player E'; },
                },
            },
        },
    },
    // ...more records...
];

document.addEventListener('DOMContentLoaded', () => {
    // 1. Directly retrieve the <template> element from the DOM
    const tpl = document.getElementById('bracket-template').content;
    const clone = tpl.cloneNode(true);

    // 5. Fill main content
    Object.keys(brackets).forEach((competition) => {
        Object.keys(brackets[competition]).forEach((level) => {
            const l = brackets[competition][level];
            Object.keys(brackets[competition][level]).forEach((round, rNum) => {
                const r = l[round];
                Object.keys(brackets[competition][level][round]).forEach((matchKey, i) => {
                    const match = r[matchKey];

                    if (level === 'winner' && round === 'round4' && matchKey === 'match1' && match.winner() === match.player1) {
                        clone.querySelector(`.GrandFinal .optional`).style.display = 'none';
                        clone.querySelector(`.GrandFinal`).style.marginTop = '170px';
                        clone.querySelector(`.GrandFinal .match`).style.marginBottom = '0px';
                    };

                    const p1MatchElement = clone.querySelector(`.round-${rNum + 1}-${level} .match${i + 1}-player1`);
                    p1MatchElement.querySelector('.player_name').id = `${match.player1}`;
                    p1MatchElement.querySelector('.player_name').innerHTML = `
                    <a href="../players" target="_parent">${match.player1}</a>`;
                    p1MatchElement.querySelector('.player_team').textContent = match.team1;
                    p1MatchElement.querySelector('.score').textContent = match.score1;

                    const p2MatchElement = clone.querySelector(`.round-${rNum + 1}-${level} .match${i + 1}-player2`);
                    p2MatchElement.querySelector('.player_name').id = `${match.player2}`;
                    p2MatchElement.querySelector('.player_name').innerHTML = `
                    <a href="../players" target="_parent">${match.player2}</a>`;
                    p2MatchElement.querySelector('.player_team').textContent = match.team2;
                    p2MatchElement.querySelector('.score').textContent = match.score2;
                });
            });
        });

        document.getElementById('bracket-container').appendChild(clone);

    });
});