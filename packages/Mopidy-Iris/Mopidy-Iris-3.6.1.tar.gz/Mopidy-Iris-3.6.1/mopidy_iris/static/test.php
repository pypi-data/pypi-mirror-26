<?php

print_r($_REQUEST);

if (isset($_GET['sleep'])){
	sleep($_GET['sleep']);
	echo "Sorry, I slept for ".$GET['sleep'];
} else {
	echo "Straight back";
}
