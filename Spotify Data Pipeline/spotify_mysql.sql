create schema spotify_db;

use spotify_db;

use spotify_db;
CREATE TABLE IF NOT EXISTS spotify_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    track_name VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255),
    popularity INT,
    duration_minutes FLOAT
)

select * from spotify_tracks;

select track_name, artist, album, popularity from spotify_tracks order by popularity desc;

select avg(popularity) as average_popularity from spotify_tracks;

select track_name, artist, duration_minutes from spotify_tracks where duration_minutes > 4.0;

select 
	    case 
            when popularity >= 80 then 'Very Popular'
            when popularity >= 50 then 'Popular'
            else 'Less Popular'
		end as popularity_range, count(*) as track_count from spotify_tracks group by popularity_range;