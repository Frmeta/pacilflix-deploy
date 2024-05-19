CREATE OR REPLACE FUNCTION check_double_review()
RETURNS TRIGGER AS 
$$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM ulasan 
        WHERE id_tayangan = NEW.id_tayangan 
        AND username = NEW.username
    ) THEN
        RAISE EXCEPTION 'User has already reviewed this show';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_ulasan_double
BEFORE INSERT ON ulasan
FOR EACH ROW
EXECUTE FUNCTION check_double_review();