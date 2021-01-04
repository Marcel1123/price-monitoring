package util.algo;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.SneakyThrows;
import util.models.APIResponseModel;
import util.models.EstimatePriceModel;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class PriceEstimationAlgorithm {
    @Getter(AccessLevel.PUBLIC)
    private APIResponseModel apiResponseModel;

    @SneakyThrows
    public void makeAPICall(EstimatePriceModel estimatePriceModel){
        URL apiUrl = new URL("http://localhost:8000/predict-new-product");
        HttpURLConnection connection = (HttpURLConnection)apiUrl.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json; utf-8");
        connection.setRequestProperty("Accept", "application/json");
        connection.setConnectTimeout(3000);
        connection.setReadTimeout(3000);
        connection.setDoOutput(true);

        OutputStream os = connection.getOutputStream();
        ObjectWriter objectWriter = new ObjectMapper().writer().withDefaultPrettyPrinter();
        System.out.println(objectWriter.writeValueAsString(estimatePriceModel));
        byte[] input = objectWriter.writeValueAsString(estimatePriceModel).getBytes(StandardCharsets.UTF_8);
        os.write(input, 0, input.length);

        int responseCode = connection.getResponseCode();

        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                        connection.getInputStream()
                )
        );

        StringBuilder response = new StringBuilder();
        String currentLine;

        while ((currentLine = in.readLine()) != null)
            response.append(currentLine);

        in.close();

        ObjectMapper objectMapper = new ObjectMapper();
        this.apiResponseModel = objectMapper.readValue(response.toString(), APIResponseModel.class);
    }
}
