package page.classes;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import entities.ProductEntity;
import lombok.Getter;
import lombok.Setter;
import lombok.SneakyThrows;
import util.models.EstimatePriceModel;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Map;

@Named
@RequestScoped
@Getter
@Setter
public class PriceEstimation {
    private EstimatePriceModel productEntity;

    @PostConstruct
    @SneakyThrows
    public void init(){
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        productEntity = (EstimatePriceModel) parameterValue.get("product");

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
        byte[] input = objectWriter.writeValueAsString(productEntity).getBytes(StandardCharsets.UTF_8);
        os.write(input, 0, input.length);

        int responseCode = connection.getResponseCode();
        System.out.println(connection);
    }
}
