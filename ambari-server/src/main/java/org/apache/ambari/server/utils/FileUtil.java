package org.apache.ambari.server.utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class FileUtil {
	private static final Log LOG = LogFactory.getLog(ShellCommandUtil.class);
	
	public static String read(String filePath){
		File file = new File(filePath);
		String fileContent = "";
		if(!file.exists()){
			LOG.error("file is not exists:"+filePath );
			return "";
		}
		BufferedReader bufferReader = null;
		try {
			bufferReader = new BufferedReader(new FileReader(file));
			String lineString = null;
			while((lineString = bufferReader.readLine()) != null){
				fileContent += lineString + "\n";
			}
		} catch (IOException e) {
			LOG.error(e.getMessage());
			e.printStackTrace();
		} finally {
			if(bufferReader != null){
				try{
					bufferReader.close();
				}catch(IOException ex){
					LOG.error(ex.getMessage());
					ex.printStackTrace();
				}
			}
		}
		return fileContent;
	}
	
	public static void main(String[] args){
		System.out.println(FileUtil.read("D:/id_rsa"));
	}
}
