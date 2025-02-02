final

JOIN users u ON p.user_id = u.id
JOIN post_user_Like l ON p.user_id = l.user_id
WHERE l.user_id = ? AND l.is_like = TRUE
GROUP BY p.id
ORDER BY p.created DESC;