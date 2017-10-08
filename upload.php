<?php
    $filelength = 5;
    $finaldir = "https://i.aurorame.me/";
    function CleanSTR($str) {
        $disallowedchars = ["\0", "\n", "\r", "*", "'", '"'];
        foreach($disallowedchars as $char) {
            $str = str_replace($char, "X", $str);
        }
        return $str;
    }
    function RandomStringGenerator($length, $db, $filetype) {
		$loop = true;
		while($loop) {
			$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
			$charactersLength = strlen($characters);
			$randomString = '';
			for ($i = 0; $i < $length; $i++) {
				$randomString .= $characters[rand(0, $charactersLength - 1)];
			}
			$sqlq = $db -> querySingle("SELECT COUNT(*) as COUNT FROM uploadlog WHERE filename = '" . $randomString . "." . CleanSTR($filetype) . "'");
			if ($sqlq == 0) {
				$loop = false;
			}
		}
        return $randomString;
    }
    if(!isset($_POST["key"])) {
        $json->status = "ERR";
        $json->errormsg = "No key found.";
    } else {
        if ($_POST["key"] == "INSERT_KEY_HERE") {
            $json->status = "ERR";
            $json->errormsg = "Invalid key.";
        } else {
            $db = new SQLite3("website.db");
            $keycleaned = CleanSTR($_POST["key"]);
            try {
                $sqlresult = $db -> querySingle("SELECT COUNT(*) as COUNT FROM keylist WHERE dkey = '" . $keycleaned . "'");
            } catch (SQLiteException $e) {
                $json->status = "ERR";
                $json->errormsg = $e;
                die(json_encode($json));
            }
            if ($sqlresult == 0) {
                $json->status = "ERR";
                $json->errormsg = "Invalid key.";
            } else {
                $allowedfiles = array('png', 'jpeg', 'jpg', 'gif', 'txt', 'bmp', 'mp3');
                $target_file = $_FILES["fileform"]["name"];
                $filetype = strtolower(end(explode(".", $target_file)));
                if (!in_array($filetype, $allowedfiles)) {
                    $json->status = "ERR";
                    $json->errormsg = "File type not allowed.";
                } else {
                    if(filesize($_FILES["fileform"]["tmp_name"]) > 10485760) {
                        $json->status = "ERR";
                        $json->errormsg = "File too big.";
                    } else {
						if(isset($_POST["file_length"])) {
							if($_POST["file_length"] >= 5 and $_POST["file_length"] <= 230) {
								$filelength = $_POST["file_length"];
							}
						}
                        $filename = RandomStringGenerator($filelength, $db, $filetype);
                        if (move_uploaded_file($_FILES["fileform"]["tmp_name"], "i/".$filename.'.'.$filetype)) {
                            $json->status = "OK";
                            $json->errormsg = "";
                            $json->url = $finaldir . $filename . '.' . $filetype;
                            $db->exec("INSERT INTO uploadlog(dkey, filename, ipaddr) VALUES ('" . $keycleaned . "', '" . $filename.".".$filetype . "', '" . $_SERVER["HTTP_CF_CONNECTING_IP"] ."')");
                        } else {
                            $json->status = "ERR";
                            $json->errormsg = "Upload failed.";
                        }
                    }
                }
            }
        }
    }
    echo(json_encode($json));
